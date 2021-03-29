// ==UserScript==
// @icon         https://ci.phncdn.com/www-static/favicon.ico
// @name         Pornhub 视频一键下载 | pornhub.com
// @namespace    https://github.com/ekoooo
// @version      0.0.9
// @description  Pornhub 视频一键下载 | pornhub.com | 无需登录直接下载 | 可直接下载免费观看付费下载视频 | 可下载已禁止下载的视频 | 可下载所有可观看分辨率
// @author       liuwanlin
// @match        *://*.pornhub.com/view_video.php?viewkey=*
// @match        *://*.pornhubpremium.com/view_video.php?viewkey=*
// @grant        unsafeWindow
// @grant        GM_setClipboard
// @grant        GM_download
// @grant        GM_addStyle
// @grant        GM_notification
// @require      https://cdn.bootcss.com/jquery/1.12.4/jquery.min.js
// ==/UserScript==

GM_addStyle(`
.download-urls ul {
    padding: 10px;
    font-weight: bold;
    line-height: 1.5;
}
.download-urls ul li {
    display: flex;
    align-items: center;
    height: 20px;
}
.download-url-label {
    text-align: right;
}
.download-url-copy {
    text-align: right;
}
.download-url-input {
    flex: 3;
    font-size: 12px;
    padding: 0 5px;
    border: 1px solid #ffff;
    margin: 0 5px;
}
`);

(function() {
    'use strict';

    const MutationObserver = unsafeWindow.MutationObserver || unsafeWindow.WebKitMutationObserver || unsafeWindow.MozMutationObserver;
    const mutationObserver = new MutationObserver(mutations => {
        mutationObserver.disconnect();
        setTimeout(() => {
            unsafeWindow.VideoParsing.init();
        }, 200);
    });
    const playerDom = document.querySelector('#player');

    if(playerDom) {
        mutationObserver.observe(playerDom, {
            childList: true,
            subtree: true,
        });
    }else {
        console.warn('视频一键下载未生效！');
    }
})();

(function() {
    var EDITOR          = 'C:\\test.bat';// \→\\
    class VideoParsing {
        // 根据 key 开头字母获取对象中的值，返回数组
        static getObjectValueByStartsWithChar(obj, char) {
            const vars = [];
            Object.keys(obj).forEach(key => {
                if(key.startsWith(char)) {
                    vars.push({
                        key: key,
                        value: obj[key],
                    });
                }
            });
            return vars;
        }

        // 获取下载地址信息，返回数组
        static getUrlInfo() {
            const flashvars = this.getObjectValueByStartsWithChar(unsafeWindow, 'flashvars_');
            if(!flashvars.length) {
                console.error('错误，未获取视频地址！', flashvars);
                return;
            }

            const qualitys = this.getObjectValueByStartsWithChar(flashvars[0].value, 'quality_');

            return qualitys.map(item => ({
                quality: item.key.replace('quality_', ''),
                url: item.value,
            }));
        }

        // 注入到下载面板
        static injectUrls2Dom(urlInfo) {
            const li = [];
            var max = 0
            urlInfo.forEach(item => {
                if(max < parseInt(item.quality))
                {
                    max = parseInt(item.quality)
                }
            });
            var title = document.title
            var titleend = title.replace(' - Pornhub.com', '.mp4')
            GM_setClipboard(encodeURIComponent(titleend), '提示')
            //console.warn(window.location.href);
            //var code = encodeURI(titleend)
            urlInfo.forEach(item => {
                if(parseInt(item.quality) == max)
                {
                    li.push(`
                        <li>
                            <a class="download-url-copy" data-href="${ item.url }" href="javascript: void(0);">复制按钮</a>
                            <span class="download-url-label">[ ${ item.quality.toUpperCase() } 分辨率 ]</span>
                            <input class="download-url-input" value="${ item.url }" />
                            <a href="WegetDonwLoad:?path=${ item.url }&out=${ encodeURIComponent(titleend) }">WegetDonwLoad</a>
                        </li>
                    `);
                    //<a href="WegetDonwLoad:?path=${ item.url }&out=${ encodeURIComponent(titleend) }">WegetDonwLoad</a>
                    //<a href="WegetDonwLoad:?path=${ window.location.href }">WegetDonwLoad</a>
                    //<a href="WegetDonwLoad:?path=${ item.url }&out=${ titleend }">WegetDonwLoad</a>
                    //<a target="_blank" class="download-url-copy" data-href="${ item.url }" href="javascript: void(0);">下载按钮</a>
                }
            });

            $('.title-container').before(`<div class="download-urls"><h3>视频下载地址：</h3><ul>${ li.join('') }</ul></div>`);
        }

        // 初始化事件
        static initEvens() {
            // 点击下载复制到粘贴板中
            $(document).on('click', '.download-url-copy', function(e) {
                e.preventDefault();
                GM_setClipboard($(this).data('href'));
                //var title = document.title
                //var titleend = title.replace(' - Pornhub.com', '.mp4')
            })
        }

        static init() {
            this.injectUrls2Dom(this.getUrlInfo());
            this.initEvens();
        }
    }

    unsafeWindow.VideoParsing = VideoParsing;
})();