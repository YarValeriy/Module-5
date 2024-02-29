import sys
from datetime import datetime, timedelta
import httpx
import asyncio
import platform

class HttpError(Exception):
    pass

async def request(url: str):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url)
        if r.status_code == 200:
            result = r.json()
            return result
        else:
            raise HttpError(f"Error status: {r.status_code} for {url}")


async def main(index_day):
    e_rates = []
    on_date = {}
    exchange = {'EUR': {"sale":0, "purchase":0}, "USD": {"sale": 0, "purchase": 0}}
    for i in range(index_day):
        d = datetime. now() - timedelta(days=int(i))
        shift = d.strftime ("%d.%m.%Y")
        try:
            response = await request (f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
            exchange["EUR"]["sale"] = response["exchangeRate"][8]["saleRate"]
            exchange["EUR"]["purchase"] = response["exchangeRate"][8]["purchaseRate"]
            exchange["USD"]["sale"] = response["exchangeRate"][23]["saleRate"]
            exchange["USD"]["purchase"] = response["exchangeRate"][23]["purchaseRate"]
            on_date[shift] = exchange
        except HttpError as err:
            print(err)
            return None
    e_rates.append(on_date)    
    return e_rates

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) < 2:
        shift = int(input("Enter N days of backtracking: "))
    else:
        shift = int(sys.argv[1])
    shift = min(shift, 10)
    r = asyncio.run(main(shift))

    print(r)
