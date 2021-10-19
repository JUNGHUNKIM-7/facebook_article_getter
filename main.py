from inputs import *
from container import Container

# --------Debug----------
# 1. Search keyword 버튼 클릭 문제
# Element <div class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p"> could not be scrolled into view
# 2. 2020 이하 버튼 클릭 문제
# no found any btn
# --------Debug----------

if __name__ == '__main__':
    with Container.make_instance(key='facebook', **fb) as fb_ins, \
            Container.make_instance(key='yh', news_channel='world', **news) as news_ins, \
            Container.switch_fb_run(run=True):
        if not Container.run_fb:
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
                Container.run_facebook(instance=fb_ins, year=2020, drag_count_or_infinite=1, root='files',
                                       file_name='oh',
                                       kind='txt')
                # Container.extracting_keyword()
                # Container.run_investing()
                # Container.news_run()
            except Exception as e:
                print(e)
