import logging
import os
# 打印log到本地

class Debug:
	def InitLogger(self,logPath):
		self.logger = logging.getLogger('log')
		self.logger.setLevel(logging.DEBUG)
		curLogPath = logPath + '/log.log'
		if os.path.exists(curLogPath):
		    os.remove(curLogPath)
		fh = logging.FileHandler(curLogPath,encoding='utf-8')
		fh.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	def Log(self,str):
		self.logger.info(str)
