from flask import Flask, render_template, request
import os

app = Flask(__name__)
path = os.path.dirname(__file__) + "\\static\\movies"   # 视频资源存放位置


@app.route('/')
def index():
    selected_category = request.args.get("category")
    category_nums = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]  # 所有分区的编号
    category_key = []   # 所有分区名称
    
    for name in category_nums:
        with open(path + "\\" + name + "\\title.txt", 'r', encoding='utf-8') as file:
            category_key.append(file.read())
    
    category_val = [(request.host_url + "?category=" + name) for name in category_nums]
    c = dict(zip(category_key, category_val))
    
    if selected_category in category_nums:
        category_path = path + "\\" + selected_category
        
        video_nums = [name for name in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, name))]   # 分区内视频编号
        video_key = []  # 分区内所有视频标题
        
        for name in video_nums:
            with open(category_path + "\\" + name + "\\title.txt", 'r', encoding='utf-8') as file:
                video_key.append(file.read())
                file.close()
        
        video_url = [(request.host_url + "player/" + "?category=" + selected_category + "&video=" + name) for name in video_nums]
        video_cover = [(request.host_url + "static/movies/" + selected_category + "/" + name + "/cover.png") for name in video_nums]
        video_val = list(zip(video_url, video_cover))
        
        v = dict(zip(video_key, video_val)) 
        return render_template("index.html", categories=c, name=category_key[int(selected_category)], videos=v)
    else:
        return render_template("index.html", categories=c, name="", videos={})
    

@app.route('/search/')
def search():
    q = request.args.get("query")
    category_nums = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    print(category_nums)
    
    # 存储符合搜索条件的视频名称，资源地址和封面
    query_video_key = []
    query_video_url = []
    query_video_cover = []
    
    for c_num in category_nums:
        category_path = path + "\\" + str(c_num)
        video_nums = [name for name in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, name))]
        
        for v_num in video_nums:
            with open(category_path + "\\" + str(v_num) + "\\title.txt", 'r', encoding='utf-8') as file:
                video_name = file.read()
                file.close()
                if q.strip().lower() in video_name.strip().lower():
                    query_video_key.append(video_name)
                    query_video_url.append(request.host_url + "player/" + "?category=" + str(c_num) + "&video=" + str(v_num))
                    query_video_cover.append(request.host_url + "static/movies/" + str(c_num) + "/" + str(v_num) + "/cover.png")

    query_video_val = list(zip(query_video_url, query_video_cover))
        
    v = dict(zip(query_video_key, query_video_val))
    return render_template("search.html", query=q, videos=v, total=len(v))
    

@app.route('/player/')
def play():
    c = request.args.get("category")
    v = request.args.get("video")
    
    video_path = request.host_url + "static/movies/" + c + "/" + v + "/video.mp4"
    
    with open(path + "\\" + c + "\\" + v + "\\title.txt", 'r', encoding='utf-8') as file:
        t = file.read()
    
    return render_template("player.html", title=t, source=video_path, link=video_path)


@app.route('/upload/')
def upload():
    category_nums = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    category_key = []
    
    for name in category_nums:
            with open(path + "\\" + name + "\\title.txt", 'r', encoding='utf-8') as file:
                category_key.append(file.read())
    return render_template("upload.html", categories=category_key, length=len(category_key))
        
    
@app.route('/submit/', methods=["POST"])
def submit():
    category = request.form.get("category")
    name = request.form.get("name")
    
    file_vid = request.files['vid']
    file_pic = request.files['pic']
    
    category_path = path + "\\" + str(category)
    video_num = len([name for name in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, name))])
    video_path = category_path + "\\" + str(video_num)
    
    # 先确保视频存在再加载标题，封面
    if file_vid:
        os.makedirs(video_path, exist_ok=True)
        file_vid.save(video_path + "\\video.mp4")
        with open(video_path + "\\title.txt", "w", encoding='utf-8') as file:
            file.write(name)
            file.close()
        
        if file_pic:
            file_pic.save(video_path + "\\cover.png")
    
    
    with open(path + "\\" + category + "\\title.txt", 'r', encoding='utf-8') as file:
        category_name = file.read()
    
    return render_template("submit.html", name=name, category_name=category_name)


@app.route('/edit/', methods=['GET'])
def edit():
    mode = request.args.get("mode")
    if mode == "new_category":
        val = request.args.get("val")
        category_num = len([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
        category_path = path + "\\" + str(category_num)
        
        os.makedirs(category_path, exist_ok=True)
        with open(category_path + "\\title.txt", "w", encoding="utf-8") as file:
            file.write(val)
            file.close()
    
    return render_template("edit.html")
     