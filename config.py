import configparser


def returnConfig():
	config = configparser.ConfigParser()
	config.read("conf.ini")
	return config