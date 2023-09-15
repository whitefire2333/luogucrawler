from bs4 import BeautifulSoup
from tkinter import ttk, messagebox, Scrollbar, Listbox
import random
import os
import re
import time
import urllib.parse
import tkinter as tk
import requests
import json
import jsonpath
import threading
cookie = {
    'login_referer': 'https%3A%2F%2Fwww.luogu.com.cn%2Fauth%2Flogin',
    '_uid': '1093109',
    '__client_id': '8d5b5aee465ecbb743d6eaf1b47a61b5895fc9a2',
    'C3VK': '43a082',
}

def start_work(anum, bnum):
    create_progress_window()
    print("正在爬取info...")
    text_output.insert(tk.END, "正在爬取info...\n")
    text_output.see(tk.END)
    Get_info(anum, bnum)
    print("info爬取成功！")
    text_output.insert(tk.END, "info爬取成功！\n")
    text_output.see(tk.END)
    bnum += 1
    # problemID为题目编号，从1000开始到8000结束
    for problemID in range(anum, bnum):

        time.sleep(random.randint(1, 3))

        # 获取url 格式为 https://www.luogu.com.cn/problem/P+题目编号
        url = 'https://www.luogu.com.cn/problem/P' + str(problemID)

        title = Get_Problem_title(problemID)
        print('题目标题：' + str(title))
        text_output.insert(tk.END, '题目标题：' + str(title) + '\n')
        text_output.see(tk.END)
        print('正在爬取题目...')
        text_output.insert(tk.END, '正在爬取题目...\n')
        text_output.see(tk.END)
        with open('user_agents.txt', 'r') as f:
            lines = f.readlines()
            custom_user_agent = random.choice(lines).strip()
        # 设置请求头
        headers = {
            'User-Agent': custom_user_agent,
        }
        r = requests.get(url, headers=headers, cookies=cookie)
        html = r.text

        # 文件夹名不能包含\ / : * ? " < > |,
        # 而标题（title）可能会包含这些字符，导致文件夹创建失败
        strT7 = str(title).replace(':', ' ')
        strT6 = strT7.replace('\\', '')
        strT5 = strT6.replace('/','')
        strT4 = strT5.replace('?', '')
        strT3 = strT4.replace('<', '小于')
        strT2 = strT3.replace('>', '大于')
        strT1 = strT2.replace('|', ' ')
        strT = strT1.replace('*', 'x')

        # 判断是否爬取成功
        if html == 'error':
            print('题目爬取失败！')
            text_output.insert(tk.END, '题目爬取失败！\n')
            text_output.see(tk.END)
        else:
            problemMD = Get_MD(html)
            print("获取题目MD文件成功！")
            text_output.insert(tk.END, "获取题目MD文件成功！\n")
            text_output.see(tk.END)
            filename = 'P' + str(problemID) + '-' + strT + '.md'

            if not os.path.exists('data/' + 'P' + str(problemID) + '-' + strT):
                os.mkdir('data/' + 'P' + str(problemID) + '-' + strT)
                print('已创建文件夹：P' + str(problemID) + '-' + str(title))
                text_output.insert(tk.END, '已创建文件夹：P' + str(problemID) + '-' + strT + '\n')
                text_output.see(tk.END)
            else:
                print('文件夹已存在，无需创建！')
                text_output.insert(tk.END, '文件夹已存在，无需创建！\n')
                text_output.see(tk.END)
            # 将文件保存到data目录下
            with open('data/' + 'P' + str(problemID) + '-' + strT + '/' + filename, 'w', encoding='utf-8') as f:
                f.write(problemMD)
            # 打印提示信息
            print('题目爬取成功！')
            text_output.insert(tk.END, '题目爬取成功！\n')
            text_output.see(tk.END)

        # 开始爬取题解
        print("正在爬取题解...")
        text_output.insert(tk.END, "正在爬取题解...\n")
        text_output.see(tk.END)
        # 获取题解url
        url = 'https://www.luogu.com.cn/problem/solution/P' + str(problemID)

        # 创建请求
        r = requests.get(url, headers=headers, cookies=cookie)
        # 获取网页内容
        html = r.text
        # 判断是否爬取成功
        if html == 'error':
            print("题解爬取失败！")
            text_output.insert(tk.END, "题解爬取失败！\n")
            text_output.see(tk.END)
        else:
            solutionMD = Get_TJ_MD(html)
            print("获取题解MD文件成功！")
            text_output.insert(tk.END, "获取题解MD文件成功！\n")
            text_output.see(tk.END)
            filename = 'P' + str(problemID) + '-' + strT + '-题解.md'
            with open('data/' + 'P' + str(problemID) + '-' + strT + '/' + filename, 'w', encoding='utf-8') as f:
                f.write(solutionMD)
            print('题解爬取成功！')
            text_output.insert(tk.END, '题解爬取成功！\n')
            text_output.see(tk.END)
    update_database_info()
    print('\n')
    print('所有题目爬取完毕！')
    text_output.insert(tk.END, '\n')
    text_output.see(tk.END)

    close_progress_window()
    messagebox.showinfo(title='提示', message='所有题目爬取完毕！')
# 创建函数，用于切换页面
def show_frame(frame, window_size=None):
    frame.tkraise()

    # 如果提供了窗口尺寸，就使用它来设置窗口大小
    if window_size:
        root.geometry(window_size)
def center_widgets(frame):
    def start_button_click():
        global progress_window
        left_range = left_range_entry.get()
        right_range = right_range_entry.get()
        try:
            left_range = int(left_range)
            right_range = int(right_range)
            if left_range < 1000 or 8000 < right_range < left_range:
                # 如果题号不在有效范围内，弹出错误提示框
                messagebox.showerror("错误", "题号范围无效，请输入1000-8000之间的题号，且开始题号不能大于结束题号")
                return
        except ValueError:
            # 如果输入的不是整数，弹出错误提示框
            messagebox.showerror("错误", "请输入有效的整数题号")
            return
        # 启动爬虫线程
        crawl_thread = threading.Thread(target=lambda: start_work(left_range, right_range))
        crawl_thread.start()

    inner_frame = tk.Frame(frame)
    inner_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    left_range_label = tk.Label(inner_frame, text="开始题号:")
    left_range_label.grid(row=0, column=0, pady=9)
    left_range_entry = tk.Entry(inner_frame)
    left_range_entry.grid(row=0, column=1, pady=9)

    right_range_label = tk.Label(inner_frame, text="结束题号:")
    right_range_label.grid(row=1, column=0, pady=9)
    right_range_entry = tk.Entry(inner_frame)
    right_range_entry.grid(row=1, column=1, pady=9)

    start_button = tk.Button(inner_frame, text="开爬", command=start_button_click)
    start_button.grid(row=2, column=0, columnspan=2, pady=9)

    # 配置内部 Frame 的列和行以使其自适应居中
    inner_frame.columnconfigure(0, weight=1)
    inner_frame.columnconfigure(1, weight=1)
    inner_frame.rowconfigure(0, weight=1)
    inner_frame.rowconfigure(1, weight=1)
    inner_frame.rowconfigure(2, weight=1)
# 编写搜索函数
def perform_search():
    global difficulty_var, source_options, keyword_entry, result_text, source_vars, source_listbox
    # 从 info.json 文件中读取题目数据
    def load_problem_data():
        try:
            with open('info.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    DFP = load_problem_data()

    # 获取用户选择的标签选项
    selected_tags_indices = source_listbox.curselection()
    selected_tags = [source_options[i] for i in selected_tags_indices]

    # 获取用户选择的难度、标签和关键词
    selected_difficulty = difficulty_var.get()
    keyword = keyword_entry.get().lower()  # 转换为小写，方便不区分大小写搜索

    # 清空之前的搜索结果
    result_text.delete(1.0, tk.END)

    # 初始化一个变量，用于检测是否找到了匹配的题目
    found = False

    # 遍历题目数据，根据用户选择和关键词进行筛选
    for PRO in DFP:
        DP = selected_difficulty == "所有难度" or selected_difficulty == PRO["难度"]
        TP = not selected_tags or any(tag in selected_tags for tag in PRO["标签"])
        KP = not keyword or keyword in PRO["题目"].lower() or any(
            keyword in tag.lower() for tag in PRO["标签"])

        # 如果所有条件匹配，将题目信息添加到结果中
        if DP and TP and KP:
            result_text.insert(tk.END,
                               f"题号：{PRO['题号']}\n题目：{PRO['题目']}\n难度：{PRO['难度']}\n标签：{', '.join(PRO['标签'])}\n\n")
            found = True  # 找到匹配的题目

    # 如果未找到内容，弹出提示框，并将所有选择清空
    if not found:
        messagebox.showinfo("未找到", "未找到匹配的题目。")
        # 清空选择
        difficulty_var.set("所有难度")
        source_listbox.selection_clear(0, tk.END)  # 清除标签多选框的选择
        keyword_entry.delete(0, tk.END)  # 清空关键词搜索框

# 从info.json文件中读取标签种类
def get_tags_from_json():
    try:
        with open('info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            tags_set = set()  # 使用集合来存储不同的标签
            for item in data:
                tags_set.update(item['标签'])
            return list(tags_set)
    except FileNotFoundError:
        return []


# 编写函数来获取用户选择的标签
def get_selected_tags():
    # 获取标签选项
    source_options = get_tags_from_json()
    selected_tags = [source_options[i] for i, var in enumerate(source_vars) if var.get()]
    return selected_tags

def clear_database():
    # 弹出确认提示框
    confirm = messagebox.askokcancel("确认清空", "要清空数据库吗？")

    if confirm:
        # 获取 data 目录的路径
        data_directory = "./data"

        # 检查 data 目录是否存在
        if os.path.exists(data_directory):
            # 遍历 data 目录下的所有文件和子目录，并删除它们
            for item in os.listdir(data_directory):
                item_path = os.path.join(data_directory, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    for sub_item in os.listdir(item_path):
                        sub_item_path = os.path.join(item_path, sub_item)
                        os.remove(sub_item_path)
                    os.rmdir(item_path)

            # 清空 info.json 文件
            info_json_path = "./info.json"
            if os.path.exists(info_json_path):
                os.remove(info_json_path)

            messagebox.showinfo("数据清空", "数据和 info.json 文件已成功清空。")

            # 更新数据库信息
            update_database_info()
        else:
            messagebox.showwarning("目录不存在", "data 目录不存在，无法清空数据库。")



global difficulty_var, source_options, keyword_entry, result_text, source_vars, database_info_label, source_listbox, progress_window, progress_label, progress_bar, text_output, progress_bar
original_window_size = "400x200"
# 创建窗口显示进度

# 获取json格式的数据包
def Get_info(anum, bnum):
    headers = {
        "authority": "www.luogu.com.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
        "Cookie": "__client_id=8d5b5aee465ecbb743d6eaf1b47a61b5895fc9a2; _uid=1093109",
    }
    tag_url = 'https://www.luogu.com.cn/_lfe/tags'
    tag_html = requests.get(url=tag_url, headers=headers).json()
    tags_dicts = []
    tags_tag = list(jsonpath.jsonpath(tag_html, '$.tags')[0])
    for tag in tags_tag:
        if jsonpath.jsonpath(tag, '$.type')[0] != 1 or jsonpath.jsonpath(tag, '$.type')[0] != 4 or \
                jsonpath.jsonpath(tag, '$.type')[0] != 3:
            tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})
    arr = ['暂无评定', '入门', '普及−', '普及/提高−', '普及+/提高',
           '提高+/省选−', '省选/NOI−', 'NOI/NOI+/CTSC']
    ts = []
    a = (anum - 1000) // 50 + 1
    b = (bnum - 1000) // 50 + 1
    for page in range(a, b + 1):
        # page = 1
        url = f'https://www.luogu.com.cn/problem/list?page={page}'
        html = requests.get(url=url, headers=headers).text
        urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
        htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
        result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])
        for res in result:
            pid = jsonpath.jsonpath(res, '$.pid')[0]
            # 定义id,将题目id中的P去掉
            id = pid[1:]
            # 当id小于anum时，跳过本次循环
            if int(id) < anum:
                continue
            # 当id大于bnum时，跳出循环
            if int(id) > bnum:
                break
            title = jsonpath.jsonpath(res, '$.title')[0]
            difficulty = arr[int(jsonpath.jsonpath(res, '$.difficulty')[0])]
            tags_s = list(jsonpath.jsonpath(res, '$.tags')[0])
            tags = []
            for ta in tags_s:
                for tags_dict in tags_dicts:
                    if tags_dict.get('id') == ta:
                        tags.append(tags_dict.get('name'))
            wen = {
                "题号": pid,
                "题目": title,
                "标签": tags,
                "难度": difficulty
            }
            ts.append(wen)
        # 将数据写入JSON文件
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(ts, f, ensure_ascii=False, indent=4)
def Get_MD(html):
    bs = BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md
def Get_TJ_MD(html):
    soup = BeautifulSoup(html, "html.parser")
    encoded_content_element = soup.find('script')
    encoded_content = encoded_content_element.text
    start = encoded_content.find('"')
    end = encoded_content.find('"', start + 1)
    encoded_content = encoded_content[start + 1:end]
    decoded_content = urllib.parse.unquote(encoded_content)
    decoded_content = decoded_content.encode('utf-8').decode('unicode_escape')
    start = decoded_content.find('"content":"')
    end = decoded_content.find('","type":"题解"')
    decoded_content = decoded_content[start + 11:end]
    return decoded_content
# 创建标题获取函数，将problemID作为参数传入
def Get_Problem_title(problemID):
    # 生成要访问的url
    url = 'https://www.luogu.com.cn/problem/P' + str(problemID)
    print('----------- 正在爬取 ' + str(problemID) + ' ------------')
    text_output.insert(tk.END, '----------- 正在爬取 ' + str(problemID) + ' ------------\n')
    text_output.see(tk.END)
    # 从user_agents.txt里随机选择一行，作为本次请求的User-Agent
    with open('user_agents.txt', 'r') as f:
        lines = f.readlines()
        custom_user_agent = random.choice(lines).strip()
    # 设置请求头
    headers = {
        'User-Agent': custom_user_agent,
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('title').text
    title = title.split('-')[0]
    title = title.strip()
    return title

def create_progress_window():
    global progress_window, progress_bar, text_output, progress_label
    progress_window = tk.Toplevel(root)
    progress_window.title("爬取进度")
    progress_window.geometry("400x200")
    progress_label = tk.Label(progress_window, text="爬取中，请稍候...")
    progress_label.pack()
    # 创建输出文本框
    text_output = tk.Text(progress_window, wrap=tk.WORD)
    text_output.pack(fill=tk.BOTH, expand=True)
def close_progress_window():
    if progress_window and progress_window.winfo_exists():
        progress_window.destroy()
def update_database_info():
    global database_info_label
    # 从 data 目录中获取文件夹的数量
    data_directory = "./data"
    if os.path.exists(data_directory):
        num_of_folders = len(
            [name for name in os.listdir(data_directory) if os.path.isdir(os.path.join(data_directory, name))])
    else:
        num_of_folders = 0

    global database_info_label
    # 更新数据库信息文本
    database_info_label.config(text=f"数据条数: {num_of_folders}")

def build_page2():
    global difficulty_var, source_options, keyword_entry, result_text, source_vars, database_info_label, source_listbox

    # 设置窗口尺寸
    root.geometry("300x600")

    # 创建筛选页面
    page2_frame = tk.Frame(container)
    page2_frame.grid(row=0, column=0, sticky="nsew")
    page2_frame.configure(background='white')

    # 在数据管理界面上添加返回首页按钮
    back_to_main_page2 = tk.Button(page2_frame, text="返回首页", command=return_to_main_page)
    back_to_main_page2.grid(row=0, column=0, pady=10)

    # 创建一个 LabelFrame 来组织难度和标签选择框
    filter_frame = tk.LabelFrame(page2_frame, text="筛选条件")
    filter_frame.grid(row=1, column=0, padx=20, pady=10, columnspan=3,sticky="nw")

    # 创建难度选择框
    difficulty_label = tk.Label(filter_frame, text="选择题目难度:")
    difficulty_label.grid(row=0, column=0, padx=5, pady=5)
    difficulty_var = tk.StringVar()
    difficulty_var.set("所有难度")  # 默认值
    difficulty_option = tk.OptionMenu(filter_frame, difficulty_var, "暂无评定", "入门", "普及−", "普及/提高−",
                                      "普及+/提高", "提高+/省选−", "省选/NOI−", "NOI/NOI+/CTSC")
    difficulty_option.grid(row=0, column=1, padx=5, pady=5)

    # 创建标签多选框和滚动条
    source_label = tk.Label(filter_frame, text="选择标签:")
    source_label.grid(row=1, column=0, padx=5, pady=5)

    source_scrollbar = Scrollbar(filter_frame, orient=tk.VERTICAL)
    source_scrollbar.grid(row=1, column=2, pady=5, sticky="ns")

    source_listbox = Listbox(filter_frame, selectmode=tk.MULTIPLE, yscrollcommand=source_scrollbar.set)
    source_listbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # 获取标签选项并将其添加到 Listbox 中
    source_options = get_tags_from_json()
    for option in source_options:
        source_listbox.insert(tk.END, option)

    source_scrollbar.config(command=source_listbox.yview)

    # 创建关键词搜索框
    keyword_label = tk.Label(page2_frame, text="关键词搜索:")
    keyword_label.grid(row=2, column=0, padx=20, pady=0)
    keyword_entry = tk.Entry(page2_frame)
    keyword_entry.grid(row=2, column=1, padx=30, pady=0,columnspan=2)

    # 搜索按钮
    search_button = tk.Button(page2_frame, text="搜索", command=perform_search)
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    # 结果显示区域
    result_text = tk.Text(page2_frame, wrap=tk.WORD, width=40, height=10)
    result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    return page2_frame


# 爬虫界面
def build_page1():
    global database_info_label
    # 设置窗口尺寸
    root.geometry("300x200")
    # 创建子页面1（爬虫界面）
    page1_frame = tk.Frame(container)
    page1_frame.configure(background='white')
    page1_frame.grid(row=0, column=0, sticky="nsew")  # 使用 grid 布局管理器

    # 在爬虫界面上添加返回首页按钮
    back_to_main_page1 = tk.Button(page1_frame, text="返回首页", command=return_to_main_page)
    back_to_main_page1.grid(row=0, column=0, pady=10)
    # 创建输入框和按钮
    center_widgets(page1_frame)
    return page1_frame

# 在主页面上添加返回首页按钮
def return_to_main_page():
    root.geometry("261x200")
    root.configure(background='white')
    show_frame(main_frame)

# 主函数，程序的开始
if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("洛谷爬虫")
    root.geometry("261x200")

    # 创建一个容器，用于承载不同的页面
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)
    # 创建主页面
    main_frame = tk.Frame(container)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.configure(background='white')
    # 添加标题标签
    title_label = tk.Label(main_frame, text="洛谷爬虫", font=("华文新魏", 28), padx=10, pady=10)
    title_label.configure(background='white')
    title_label.grid(row=0, column=0, columnspan=3)  # 使用 grid 布局管理器，跨3列，好看’
    # 在主页面上添加按钮，用于进入爬虫和筛选
    crawler_button = ttk.Button(main_frame, text="进入爬虫", command=lambda: show_frame(build_page1()))
    crawler_button.grid(row=1, column=0, pady=20)

    data_management_button = ttk.Button(main_frame, text="筛选", command=lambda: show_frame(build_page2()))
    data_management_button.grid(row=1, column=1, pady=20)

    # 创建一个清空数据库按钮，并绑定到clear_database函数
    clear_database_button = ttk.Button(main_frame, text="清空", command=clear_database)
    clear_database_button.grid(row=1, column=2, pady=20)

    # 创建一个 Label 组件来显示数据条数
    database_info_label = tk.Label(main_frame, text="数据条数: 0")
    database_info_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ne")
    database_info_label.configure(background='white')
    # 初始化数据库信息标签
    update_database_info()

    # 初始显示主页面
    show_frame(main_frame)

    # 运行主循环
    root.mainloop()
