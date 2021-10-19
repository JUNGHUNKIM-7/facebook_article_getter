from inputs import *
from container import Container

# ------Debug-------
# 2. 2020 이하 버튼 클릭 문제
# no found any btn
# ------Debug-------

# -----instance-----
fb_ins = Container.make_instance(key='facebook', **fb)
news_ins = Container.make_instance(key='yh', news_channel='world', **news)
# -----instance-----


if __name__ == '__main__':
    switch = Container.switch_fb_run(run=True)
    if not switch:
        try:
            pass
            # todo, 파일불러오기
            # Container.extracting_keyword()
            # Container.run_investing()
            # Container.news_run()
        except Exception as e:
            print(e)
    else:
        try:
            Container.run_facebook(instance=fb_ins,
                                   search_keyword="금리",
                                   drag_count_or_infinite=3,
                                   root='',
                                   file_name='oh',
                                   kind='txt',
                                   scrape_count=2)
            # Container.extracting_keyword()
            # Container.run_investing()
            # Container.news_run()
        except Exception as e:
            print(e)
