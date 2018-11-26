from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from users.models import User as AppUser, SubTitle, Event, Lead, Trial


def get_user_by_email(email, first_name, last_name):
    user = User.objects.filter(username=email).first()
    if not user:
        user, _ = User.objects.get_or_create(email=email, username=email)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
    return user


def get_user(first_name, last_name, email, phone, age, member_id, apk):
    user = get_user_by_email(email, first_name, last_name)
    user.save()
    app_user = AppUser.objects.filter(member_id=member_id, user=user).first()
    if not AppUser.objects.filter(member_id=member_id, user=user):
        try:
            age = int(age)
        except:
            age = 0
        app_user = AppUser.objects.create(member_id=member_id, user=user, apk=apk, age=age, phone_number=phone)
    if age:
        app_user.age = age
        app_user.save()
    return app_user


def add_sub(subscriptions, user):
    for sub in subscriptions:
        subtitle, _ = SubTitle.objects.get_or_create(title=sub.strip())
        if subtitle not in user.sub.all():
            user.sub.add(subtitle)


def add_events(events, user):
    for item in events:
        event, _ = Event.objects.get_or_create(title=item.strip())
        if event not in user.events.all():
            user.events.add(event)


def read_from_csv(content):
    for row in str(content).split('\n'):
        members = row.split('\\n')
        for index, member in enumerate(members):
            if index > 0:
                if len(member.split(',')) > 8:
                    try:
                        app_user = get_user(member.split(',')[4].strip(), member.split(',')[5].strip(),
                                            member.split(',')[7].strip(),
                                            member.split(',')[6].strip(), member.split(',')[8].strip(),
                                            member.split(',')[0].strip(),
                                            member.split(',')[2].strip())
                        subs = [m.text for m in
                                BeautifulSoup(member.split(',')[3], 'html.parser').find_all('strong')]
                        add_sub(subs, app_user)
                        events = [BeautifulSoup(member.split(',')[10], 'html.parser').text.replace('"', "").strip()]
                        add_events(events, app_user)

                    except Exception as e:
                        print(e)

    print('Successfully added element')


def get_lead(app_user, days_ago, source):
    lead, _ = Lead.objects.get_or_create(user=app_user, days_ago=days_ago, source=source)
    return lead


def add_event_in_lead(events, lead):
    for item in events:
        event, _ = Event.objects.get_or_create(title=item.strip())
        if event not in lead.event.all():
            lead.event.add(event)


def add_event_in_trial(events, trial):
    for item in events:
        event, _ = Event.objects.get_or_create(title=item.strip())
        if event not in trial.event.all():
            trial.event.add(event)


def get_trial(app_user, trial_days, subscriptions, full_name):
    trial, _ = Trial.objects.get_or_create(user=app_user, trial_days=trial_days, subscriptions_count=subscriptions,
                                           full_name=full_name)
    return trial


def read_leads_from_csv(content):
    for row in str(content).split('\n'):

        leads = row.split('\\n')
        for index, lead in enumerate(leads):
            if index > 0:
                if len(lead.split(';')) > 16:
                    try:
                        first_name = lead.split(';')[1].strip()
                        last_name = lead.split(';')[2].strip()
                        email = lead.split(';')[3].strip()
                        phone = lead.split(';')[4].strip()
                        source = lead.split(';')[8].strip()
                        member_id = lead.split(';')[11].strip()
                        events = [
                            BeautifulSoup(lead.split(';')[14], 'html.parser').text.replace('"', "").strip().split(",")[
                                0]]
                        days_ago = lead.split(';')[16].strip()
                        app_user = get_user(first_name, last_name, email, phone, 0, member_id, 0)
                        lead = get_lead(app_user, days_ago, source)
                        add_event_in_lead(events, lead)

                    except Exception as e:
                        print(e)


def read_trials_from_csv(content):
    for row in str(content).split('\n'):
        leads = row.split('\\n')
        for index, lead in enumerate(leads):
            if index > 0:
                if len(lead.split(';')) > 12:
                    try:
                        member_id = lead.split(';')[0].strip()
                        full_name = lead.split(';')[1].replace('"', '').strip()
                        age = lead.split(';')[2].replace('"', '').strip()
                        email = lead.split(';')[4].strip()
                        phone = lead.split(';')[5].strip()
                        trial_days = lead.split(';')[8].strip()
                        subscriptions = lead.split(';')[9].strip()
                        events = [
                            BeautifulSoup(lead.split(';')[11], 'html.parser').text.replace('"', "").strip().split(",")[
                                0]]

                        app_user = get_user(None, None, email, phone, age, member_id, 0)
                        trial = get_trial(app_user, trial_days, subscriptions, full_name)
                        add_event_in_trial(events, trial)

                    except Exception as e:
                        print(e)

                        # LEADS

                        # col_1: ['days_ago']
                        # col_2: ['firstname'] ['lastname'] <br>['email'] ['phone']
                        # col_3: ['events']
                        # col_4: ['source']
                        # col_5: Registration button

                        # Trials
                        # col_1: [image_url]
                        # col_2: [trial_days]
                        # col_3: [name], [subscription], [age]
                        # col_4: [phone_number]
                        # col_5: ['events']
                        # col_6: registration button
