b'<!DOCTYPE html>\n<html>\n<head>\n    <meta charset="UTF-8">\n    <meta name="full-screen" content="yes">\n    <meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">\n    <title>\xe7\x99\xbe\xe5\xba\xa6\xe6\x96\xb0\xe9\x97\xbb</title>\n\n     <!-- add CONF -->\n    <!-- ispeed\xe7\xbb\x9f\xe8\xae\xa1 -->\n\n    <link rel="stylesheet" type="text/css" href="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/n/nvn/static/news/aio_f388820.css" />\n</head>\n<body>\n    <img src="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/n/nvn/static/news/imgs/webapp-news-logo2_f77cdba.png" style="position: absolute; left: -500px; top: -500px; z-index: -100; opacity: 0.1;">\n    <div id="root"></div>    <!-- \xe5\xbe\xae\xe4\xbf\xa1\xe5\x88\x86\xe4\xba\xab -->    <!-- ispeed\xe5\x8f\x82\xe6\x95\xb0\xe9\x85\x8d\xe7\xbd\xae -->\n<script type="text/javascript" src="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/n/nvn/static/news/lib_c9c8bcf.js"></script>\n<script type="text/javascript" src="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/n/nvn/static/news/third_daa574b.js"></script>\n<script type="text/javascript" src="https://gss0.bdstatic.com/5foIcy0a2gI2n2jgoY3K/n/nvn/static/news/app_52a8674.js"></script>\n<script type="text/javascript" src="//news-bos.cdn.bcebos.com/mvideo/news-webapp-conf.js"></script>\n<script type="text/javascript">\n        /* eslint-disable */ \n\n         \n        /* dp\xe7\xbb\x9f\xe8\xae\xa1\xe7\x9b\xb8\xe5\x85\xb3\xe4\xbb\xa3\xe7\xa0\x81 */\n        window.alogObjectConfig = {\n            product: \'107\',\n            page: \'107_111\',\n\n            // \xe6\x80\xa7\xe8\x83\xbd\n            speed: {\n                sample: \'0.15\'\n            },\n\n            // js\xe5\xbc\x82\xe5\xb8\xb8\n            exception: {\n                sample: \'0.08\'\n            },\n\n            // \xe6\x96\xb0\xe7\x89\xb9\xe6\x80\xa7\n            feature: {\n                sample: \'0.08\'\n            },\n\n            csp: {\n                sample: \'0.15\',\n                \'default-src\': [\n                    {match: \'*bae.baidu.com\', target: \'Accept,Warn\'},\n                    {match: \'*.baidu.com,*.bdstatic.com,*.bdimg.com,localhost,*.hao123.com,*.hao123img.com\', target: \'Accept\'},\n                    {match: /^(127|172|192|10)(\\.\\d+){3}$/, target: \'Accept\'},\n                    {match: \'*\', target: \'Accept,Warn\'}\n                ]\n            }\n        };\n        void function(a,b,c,d,e,f,g){a.alogObjectName=e,a[e]=a[e]||function(){(a[e].q=a[e].q||[]).push(arguments)},a[e].l=a[e].l||+new Date,d="https:"===a.location.protocol?"https://fex.bdstatic.com"+d:"http://fex.bdstatic.com"+d;var h=!0;if(a.alogObjectConfig&&a.alogObjectConfig.sample){var i=Math.random();a.alogObjectConfig.rand=i,i>a.alogObjectConfig.sample&&(h=!1)}h&&(f=b.createElement(c),f.async=!0,f.src=d+"?v="+~(new Date/864e5)+~(new Date/864e5),g=b.getElementsByTagName(c)[0],g.parentNode.insertBefore(f,g))}(window,document,"script","/hunter/alog/alog.mobile.min.js","alog"),void function(){function a(){}window.PDC={mark:function(a,b){alog("speed.set",a,b||+new Date),alog.fire&&alog.fire("mark")},init:function(a){alog("speed.set","options",a)},view_start:a,tti:a,page_ready:a}}();\n        void function(n){var o=!1;n.onerror=function(n,e,t,c){var i=!0;return!e&&/^script error/i.test(n)&&(o?i=!1:o=!0),i&&alog("exception.send","exception",{msg:n,js:e,ln:t,col:c}),!1},alog("exception.on","catch",function(n){alog("exception.send","exception",{msg:n.msg,js:n.path,ln:n.ln,method:n.method,flag:"catch"})})}(window);\n\n\n        (function(d){var h="https:"===d.location.protocol?"https:":"http:",f=d.document,e;d.IS={data:{examples:{},common:{},perf:{startTime:Date.now()},perfMark:{},jserr:[],event:[]},done:function(a,b,c){var g=this.data,e=g.common,d;if(a)for(d in a)a.hasOwnProperty(d)&&(e[d]=a[d]);b=b||{};a=b.event;null==a&&(b.event={default:1});"number"===typeof a&&(b.event={default:a});g.examples=b;c=c||h+"//b.bdstatic.com/searchbox/icms/searchbox/img/common/openjs/ispeed/20170103/ispeed.min.js";c=c+"?t="+(Date.now()+"").substr(0,\n        8);b=f.createElement("script");b.type="text/javascript";b.src=c;f.head.appendChild(b)},_jsLoaded:function(){var a=this.data;a._needToSendPerfDataNow&&IS._sendPerfData();var b=a.jserr,c=b.length;if(c)for(e=0;e<c;e++)IS._httpGet("jserr",b[e]);a=a.event;if(b=a.length)for(e=0;e<b;e++)IS._httpGet("event",a[e]);IS._httpGet("pv")},sendJsErr:function(a,b){if(a){var c=this.data.jserr;b&&(a.flag="catch");0<a.msg.indexOf(":")&&(a.type=a.msg.slice(0,a.msg.indexOf(":")));this._httpGet?this._httpGet("jserr",a):\n        c.push(a)}},sendJsCatch:function(a){this.sendJsErr(a,!0)},sendEvent:function(a,b){var c=this.data.event;this._httpGet?this._httpGet("event",{evt:a,msg:b}):c.push({evt:a,msg:b})},addPerfData:function(a,b){var c=this.data;null==b&&(b=Date.now());0<b&&(c.perf[a]=b)},markPerfData:function(a,b){var c=this.data;0<b&&(c.perfMark[a]=b)},setPerfStartTime:function(a){var b=this.data;a&&(b.perf.startTime=a)},sendPerfData:function(a,b){var c=this.data,d=this._sendPerfData;d?d():c._needToSendPerfDataNow=!0}};\n        f.addEventListener("DOMContentLoaded",function(){IS.addPerfData("drt",Date.now())},!1);d.onerror=function(a,b,c,e){if(null==b||!0===/^script error/i.test(a))return!0;e=e||d.event&&d.event.errorCharacter||0;IS.sendJsErr({msg:a,js:b,ln:c,col:e})}})(window);\n    \n \n    /* eslint-disable */\n    alog(\'speed.set\', \'ht\', +new Date);\n   \n </script>\n<script type="text/javascript" src="//b.bdstatic.com/searchbox/icms/searchbox/js/common/openjs/shareconfig/2017042519/shareconfig.min.js"></script>\n<script type="text/javascript">\n        require(\'52d995e\');\n    \n\n        /* eslint-disable */\n        alog(\'speed.set\', \'drt\', +new Date);\n        IS.done({\n            page_id: \'107_001\',\n            network: \'unknown\',\n            cuid: \'\'\n        }, {\n            jserr: 1,\n            perf: .1,\n            pv: .1\n        });\n\n        void function(a,b,c,d,e,f){function g(b){a.attachEvent?a.attachEvent("onload",b,!1):a.addEventListener&&a.addEventListener("load",b)}function h(a,c,d){d=d||15;var e=new Date;e.setTime((new Date).getTime()+1e3*d),b.cookie=a+"="+escape(c)+";path=/;expires="+e.toGMTString()}function i(a){var c=b.cookie.match(new RegExp("(^| )"+a+"=([^;]*)(;|$)"));return null!=c?unescape(c[2]):null}function j(){var a=i("PMS_JT");if(a){h("PMS_JT","",-1);try{a=a.match(/{["\']s["\']:(\\d+),["\']r["\']:["\']([\\s\\S]+)["\']}/),a=a&&a[1]&&a[2]?{s:parseInt(a[1]),r:a[2]}:{}}catch(c){a={}}a.r&&b.referrer.replace(/#.*/,"")!=a.r||alog("speed.set","wt",a.s)}}if(a.alogObjectConfig){var k=a.alogObjectConfig.sample,l=a.alogObjectConfig.rand;d="https:"===a.location.protocol?"https://fex.bdstatic.com"+d:"http://fex.bdstatic.com"+d,k&&l&&l>k||(g(function(){alog("speed.set","lt",+new Date),e=b.createElement(c),e.async=!0,e.src=d+"?v="+~(new Date/864e5)+~(new Date/864e5),f=b.getElementsByTagName(c)[0],f.parentNode.insertBefore(e,f)}),j())}}(window,document,"script","/hunter/alog/dp.mobile.min.js");\n    </script>\n</body>\n</html>\n'