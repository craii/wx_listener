# - * - coding:utf-8 - * -
from wxpy import *
import logging
from time import sleep
from funcxiv import make_record_directory, generate_sql, msg_summary
from db_control import MysqlController


class WxListener(object):

    def __init__(self, listened_group, delay=10):
        self.delay = delay

        if not isinstance(listened_group, (str, list)):
            raise TypeError("群只能是字符串或由多个群组成的列表")
        self.listened_group = [u'{}'.format(listened_group)] if isinstance(listened_group, str) else listened_group
        self.record_folder = make_record_directory()
        self.db = MysqlController(db_address='localhost',
                                  db_user='root',
                                  db_pwd='jc17462315',
                                  db_name='message')

    @staticmethod
    def logger():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s：：：')
        logger = logging.getLogger(__name__)
        return logger

    def start_listen(self):

        bot = Bot(cache_path=True)

        groups = [ensure_one(bot.groups().search(group)) for group in self.listened_group]
        # groups = [bot.groups().search(group) for group in self.listened_group]

        @bot.register(groups, except_self=False)
        def listen_group(msg):
            WxListener.logger().info(f"{msg.member.name} 发送了一条【{msg.type}】消息:{msg}")

            if msg.type == 'Text':
                print(msg.raw)
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=msg.text,
                                    msg_type=TEXT,
                                    src='None')
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<文本{msg.text}> 内容插入结果{result}")

            if msg.type == 'Map':
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=msg.raw['Url'],
                                    msg_type=MAP,
                                    src='None')
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<地图内容{msg.raw['Url']}> 内容插入结果{result}")

            if msg.type == 'Sharing':
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=msg.raw['Url'],
                                    msg_type=SHARING,
                                    src='None')
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<分享链接{msg.raw['Url']}> 内容插入结果{result}")

            if msg.type == 'Picture':
                saved_to = self.record_folder + "/" + msg.file_name
                msg.get_file(saved_to)
                sleep(self.delay)
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=f"分享了一张图片<{msg.file_name}>",
                                    msg_type=PICTURE,
                                    src=saved_to)
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<图片：{msg.file_name}> 内容插入结果{result}")

            if msg.type == 'Recording':
                saved_to = self.record_folder + "/" + msg.file_name
                msg.get_file(saved_to)
                sleep(self.delay)
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=f"发送了一条语音消息<{msg.file_name}>",
                                    msg_type=RECORDING,
                                    src=saved_to)
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<语音：{msg.file_name}> 内容插入结果{result}")

            if msg.type == 'Video':
                saved_to = self.record_folder + "/" + msg.file_name
                msg.get_file(saved_to)
                sleep(self.delay)
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=f"发送了一个视频<{msg.file_name}>",
                                    msg_type=VIDEO,
                                    src=saved_to)
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<视频：{msg.file_name}> 内容插入结果{result}")

            if msg.type == 'Attachment':
                saved_to = self.record_folder + "/" + msg.file_name
                msg.get_file(saved_to)
                sleep(self.delay)
                _sql = generate_sql(sender=msg.member.name,
                                    time=msg.create_time,
                                    msg=f"发送了一个附件<{msg.file_name}>",
                                    msg_type=ATTACHMENT,
                                    src=saved_to)
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<附件：{msg.file_name}> 内容插入结果{result}")

            if msg.type in ('System', 'Friends', 'Note', 'Card'):
                WxListener.logger().warning(f'【警告】暂不处理 {msg.type} 内容，请进入微信进行查看')
                print(msg)

        @bot.register(bot.file_helper, except_self=False)
        def wait_command(commands):
            print(commands)
            if commands.text.upper() in ("SUMMARY", "总览"):
                _sql = msg_summary()
                result = self.db.run(_sql)["result"]
                msg = "成员 \t\t 消息数 \n"
                for r in result:
                    msg += f"{r[0]} \t\t {r[1]} \n"
                print(msg)
                bot.file_helper.send(msg)
            if commands.type == 'Sharing':
                _sql = generate_sql(sender=commands.member.name,
                                    time=commands.create_time,
                                    msg=commands.raw['Url'],
                                    msg_type=SHARING,
                                    src='None')
                result = self.db.run(sql=_sql, write_mode=True)
                print(f"<分享链接{commands.raw['Url']}> 内容插入结果{result}")

        embed()



if __name__ in "__main__":
    ll = WxListener(["你好"])
    ll.start_listen()
