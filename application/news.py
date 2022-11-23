
class news:
  headline = ""
  image_src = ""
  link = ""
  summary = ""



def get_news(news_category):
  url = ""
  if news_category == "Latest":
    url = 'https://bdnews24.com/collection/111531'
  elif news_category == "International":
    url = 'https://bdnews24.com/world'
  elif news_category == "Education":
    url = 'https://bdnews24.com/education'
  elif news_category == "Economy":
    url = 'https://bdnews24.com/economy'
  elif news_category == "Politics":
    url = 'https://bdnews24.com/politics'
  elif news_category == "Sports":
    url = 'https://bdnews24.com/sport'
  elif news_category == "Lifestyle":
    url = 'https://bdnews24.com/lifestyle'
  elif news_category == "Science":
    url = 'https://bdnews24.com/science'
  elif news_category == "Environment":
    url = 'https://bdnews24.com/environment'








