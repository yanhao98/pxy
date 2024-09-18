from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

NPM_JS = "https://registry.npmjs.org"

@app.route('/')
def root():
    return "hello"

@app.route('/<path:url>', methods=['GET'])
def proxy(url):
    origin_url = f"{NPM_JS}/{url}"

    # 如果URL以 .tgz 结尾，直接返回 npm registry 的内容
    if url.endswith(".tgz"):
        r = requests.get(origin_url, stream=True)
        return Response(r.raw, content_type=r.headers['Content-Type'])

    # 其他路径，获取npm registry内容并做正则替换
    r = requests.get(origin_url)
    content = r.text

    # 获取当前请求的主机名
    origin = request.host_url.rstrip('/')

    # 正则替换规则，替换 `${NPM_JS}(.*?).tgz` 为 `origin}$1.tgz`
    pattern = re.compile(f"{NPM_JS}(.*?).tgz")
    replaced_content = pattern.sub(rf'{origin}\1.tgz', content)

    return Response(replaced_content, content_type=r.headers['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787)
