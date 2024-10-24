import os
import random

import django
from dateutil import tz
from faker import Faker
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intern.settings")
django.setup()

from myapp.models import Talk, User

fakegen = Faker(["ja_JP"])

def create_users(n):
    """
    ダミーのユーザーとチャットの文章を作る。
    n: 作成するユーザーの人数
    """

    users = [
        User(username=fakegen.user_name(), email=fakegen.ascii_safe_email(), img='default_de0vGYW.jpeg')
        for _ in range(n)
    ]

    User.objects.bulk_create(users, ignore_conflicts=True)

    me = User.objects.get(id=1)

    # values_list メソッドを使うと、User オブジェクトから特定のフィールドのみ取り出すことができます。
    # 返り値はユーザー id のリストになります。
    users = User.objects.exclude(id=1)

    talks = []
    for _ in range(len(users)):
        sent_talk = Talk(
            sender=me,
            recipient=random.choice(users),
            message=fakegen.text(),
            send_time=datetime.now()
        )
        received_talk = Talk(
            sender=random.choice(users),
            recipient=me,
            message=fakegen.text(),
            send_time=datetime.now()
        )
        talks.extend([sent_talk, received_talk])
    Talk.objects.bulk_create(talks, ignore_conflicts=True)

    # Talk の time フィールドは auto_now_add が指定されているため、 bulk_create をするときに
    # time フィールドが自動的に現在の時刻に設定されてしまいます。
    # 最新の 2 * len(user_ids) 個分は先ほど作成した Talk なので、これらを改めて取得し、
    # time フィールドを明示的に更新します。
    talks = Talk.objects.order_by("-send_time")[: 2 * len(users)]
    for talk in talks:
        talk.send_time = fakegen.date_time_this_year(tzinfo=tz.gettz("Asia/Tokyo"))
    Talk.objects.bulk_update(talks, fields=["send_time"])


if __name__ == "__main__":
    print("creating users ...", end="")
    create_users(900)
    print("done")