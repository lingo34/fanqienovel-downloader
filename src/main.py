import os
import shutil
import json
import time
import platform
from novel_downloaders.factory import NovelDownloaderFactory
from novel_downloaders.base import SaveMode, Config


def create_cli():
    """Create CLI interface using the NovelDownloader class"""
    print('本程序完全免费。\nGithub: https://github.com/ying-ck/fanqienovel-downloader\n作者：Yck & qxqycb')
    
    config = Config()
    downloader = NovelDownloaderFactory.create_downloader('fanqie')(config)
    
    # Check for backup
    backup_folder_path = 'C:\\Users\\Administrator\\fanqie_down_backup'
    if os.path.exists(backup_folder_path):
        choice = input("检测到备份文件夹，是否使用备份数据？1.使用备份  2.跳过：")
        if choice == '1':
            if os.path.isdir(backup_folder_path):
                source_folder_path = os.path.dirname(os.path.abspath(__file__))
                for item in os.listdir(backup_folder_path):
                    source_item_path = os.path.join(backup_folder_path, item)
                    target_item_path = os.path.join(source_folder_path, item)
                    if os.path.isfile(source_item_path):
                        if os.path.exists(target_item_path):
                            os.remove(target_item_path)
                        shutil.copy2(source_item_path, target_item_path)
                    elif os.path.isdir(source_item_path):
                        if os.path.exists(target_item_path):
                            shutil.rmtree(target_item_path)
                        shutil.copytree(source_item_path, target_item_path)
            else:
                print("备份文件夹不存在，无法使用备份数据。")
        elif choice != '2':
            print("入无效，请重新运行程序并正确输入。")
    else:
        print("程序还未备份")

    while True:
        print('\n输入书的id直接下载\n输入下面的数字进入其他功能:')
        print('''
1. 更新小说
2. 搜索
3. 批量下载
4. 设置
5. 备份
6. 退出
        ''')
        
        inp = input()
        
        if inp == '1':
            downloader.update_all_novels()
            
        elif inp == '2':
            while True:
                key = input("请输入搜索关键词（直接Enter返回）：")
                if key == '':
                    break
                results = downloader.search_novel(key)
                if not results:
                    print("没有找到相关书籍。")
                    continue
                    
                for i, book in enumerate(results):
                    print(f"{i + 1}. 名称：{book['book_data'][0]['book_name']} "
                          f"作者：{book['book_data'][0]['author']} "
                          f"ID：{book['book_data'][0]['book_id']} "
                          f"字数：{book['book_data'][0]['word_number']}")
                
                while True:
                    choice = input("请选择一个结果, 输入 r 以重新搜索：")
                    if choice == "r":
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(results):
                        chosen_book = results[int(choice) - 1]
                        downloader.download_novel(chosen_book['book_data'][0]['book_id'])
                        break
                    else:
                        print("输入无效，请重新输入。")
                        
        elif inp == '3':
            urls_path = 'urls.txt'
            if not os.path.exists(urls_path):
                print(f"未找到'{urls_path}'，将为您创建一个新的文件。")
                with open(urls_path, 'w', encoding='UTF-8') as file:
                    file.write("# 请输入小说链接，一行一个\n")
            
            print(f"\n请在文本编辑器中打开并编辑 '{urls_path}'")
            print("在文件中输入小说链接，一行一个")
            
            if platform.system() == "Windows":
                os.system(f'notepad "{urls_path}"')
            elif platform.system() == "Darwin":
                os.system(f'open -e "{urls_path}"')
            else:
                if os.system('which nano > /dev/null') == 0:
                    os.system(f'nano "{urls_path}"')
                elif os.system('which vim > /dev/null') == 0:
                    os.system(f'vim "{urls_path}"')
                else:
                    print(f"请使用任意文本编辑器手动编辑 {urls_path} 文件")
            
            print("\n编辑完成后按Enter键继续...")
            input()
            
            with open(urls_path, 'r', encoding='UTF-8') as file:
                content = file.read()
                urls = content.replace(' ', '').split('\n')
            
            for url in urls:
                if url and url[0] != '#':
                    print(f'开始下载链接: {url}')
                    status = downloader.download_novel(url)
                    if not status:
                        print(f'链接: {url} 下载失败。')
                    else:
                        print(f'链接: {url} 下载完成。')
                        
        elif inp == '4':
            print('请选择项目：1.正文段首占位符 2.章节下载间隔延迟 3.小说保存路径 4.小说保存方式 5.设置下载线程数')
            inp2 = input()
            if inp2 == '1':
                tmp = input('请输入正文段首占位符(当前为"%s")(直接Enter不更改)：' % config.kgf)
                if tmp != '':
                    config.kgf = tmp
                config.kg = int(input('请输入正文段首占位符数（当前为%d）：' % config.kg))
            elif inp2 == '2':
                print('由于迟过小造成的后果请自行负责。\n请输入下载间隔随机延迟')
                config.delay[0] = int(input('下限（当前为%d）（毫秒）：' % config.delay[0]))
                config.delay[1] = int(input('上限（当前为%d）（毫秒）：' % config.delay[1]))
            elif inp2 == '3':
                print('tip:设置为当前目录点取消')
                time.sleep(1)
                path = input("\n请输入保存目录的完整路径:\n(直接按Enter使用当前目录)\n").strip()
                if path == "":
                    config.save_path = os.getcwd()
                else:
                    if not os.path.exists(path):
                        try:
                            os.makedirs(path)
                            config.save_path = path
                        except:
                            print("无法创建目录，将使用当前目录")
                            config.save_path = os.getcwd()
                    else:
                        config.save_path = path
            elif inp2 == '4':
                print('请选择：1.保存为单个 txt 2.分章保存 3.保存为 epub 4.保存为 HTML 网页格式 5.保存为 LaTeX')
                inp3 = input()
                try:
                    config.save_mode = SaveMode(int(inp3))
                except ValueError:
                    print('请正确输入!')
                    continue
            elif inp2 == '5':
                config.xc = int(input('请输入下载线程数：'))
            else:
                print('请正确输入!')
                continue
            
            # Save config
            with open(downloader.config_path, 'w', encoding='UTF-8') as f:
                json.dump({
                    'kg': config.kg,
                    'kgf': config.kgf,
                    'delay': config.delay,
                    'save_path': config.save_path,
                    'save_mode': config.save_mode.value,
                    'space_mode': config.space_mode,
                    'xc': config.xc
                }, f)
            print('设置完成')
            
        elif inp == '5':
            downloader.backup_data('C:\\Users\\Administrator\\fanqie_down_backup')
            print('备份完成')
            
        elif inp == '6':
            break
            
        else:
            # Try to download novel directly
            if downloader.download_novel(inp):
                print('下载完成')
            else:
                print('请输入有效的选项或书籍ID。')

if __name__ == "__main__":
    create_cli()
