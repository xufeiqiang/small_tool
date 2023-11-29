import speech_recognition as sr
from homework.logger import Logger
from homework.utils import Utils


class InputVoice:
    def __init__(self):
        log = Logger(filename=Utils.getRootPath() + '/log/smallTool.log')
        self.logger = log.logger
        # 初始化语音识别器
        self.recognizer = sr.Recognizer()

    def start_voice(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)  # 使用 Google Web API 进行语音识别
                self.logger.info("识别结果: " + text)
                return text
            except sr.UnknownValueError:
                self.logger.error("无法识别语音")
            except sr.RequestError as e:
                self.logger.error("请求错误: {0}".format(e))
