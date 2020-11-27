import configparser


def returnConfig():
	config = configparser.ConfigParser()
	config.read("config.ini")
	return config