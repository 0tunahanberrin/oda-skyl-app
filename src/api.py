import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://calendar.google.com/calendar/u/0/embed?src=bc6edfd480bce7cd796fdc737fb81ea97053ac5d51208e1cff1f04bb46168f1b@group.calendar.google.com&ctz=Europe/Istanbul']

def authenticate_google_calendar():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_events_on_date(service, calendar_id, target_date):
    start_datetime = datetime.combine(target_date, datetime.min.time())
    end_datetime = datetime.combine(target_date, datetime.max.time())

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_datetime.isoformat() + 'Z',
        timeMax=end_datetime.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return events

'''def check_custom_condition(event):
    # Özel bir durumu kontrol etmek için bu fonksiyonu düzenleyebilirsiniz.
    # Örneğin, etkinliğin adına, katılımcı sayısına veya başka bir özelliğine göre kontrol edebilirsiniz.
    return 'özel koşul' in event.get('summary', '').lower()
'''

def main():
    creds = authenticate_google_calendar()
    service = build('calendar', 'v3', credentials=creds)

    calendar_id = 'primary'

    # Kullanıcıdan tarih al
    user_input_date = input("Etkinlikleri kontrol etmek istediğiniz tarihi girin (YYYY-MM-DD): ")
    target_date = datetime.strptime(user_input_date, '%Y-%m-%d').date()

    events = get_events_on_date(service, calendar_id, target_date)

    for event in events:
        event_summary = event.get('summary', 'Bilgi Yok')
        event_start = event.get('start', {}).get('dateTime', 'Bilgi Yok')

        if check_custom_condition(event):
            print(f"{event_start}: {event_summary} - Özel Durum Doğrulandı")
        else:
            print(f"{event_start}: {event_summary} - Özel Durum Doğrulanmadı")

if __name__ == '__main__':
    main()