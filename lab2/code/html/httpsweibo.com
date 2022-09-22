b'<!DOCTYPE html>\n<html>\n<head>\n    <meta http-equiv="Content-type" content="text/html; charset=gb2312"/>\n    <title>Sina Visitor System</title>\n</head>\n<body>\n<span id="message"></span>\n<script type="text/javascript" src="/js/visitor/mini_original.js?v=20161116"></script>\n<script type="text/javascript">\n    window.use_fp = "1" == "1"; // \xca\xc7\xb7\xf1\xb2\xc9\xbc\xaf\xc9\xe8\xb1\xb8\xd6\xb8\xce\xc6\xa1\xa3\n    var url = url || {};\n    (function () {\n        this.l = function (u, c) {\n            try {\n                var s = document.createElement("script");\n                s.type = "text/javascript";\n                s[document.all ? "onreadystatechange" : "onload"] = function () {\n\n                    if (document.all && this.readyState != "loaded" && this.readyState != "complete") {\n                        return\n                    }\n                    this[document.all ? "onreadystatechange" : "onload"] = null;\n                    this.parentNode.removeChild(this);\n                    if (c) {\n                        c()\n                    }\n                };\n                s.src = u;\n                document.getElementsByTagName("head")[0].appendChild(s)\n            } catch (e) {\n            }\n        };\n    }).call(url);\n\n    // \xc1\xf7\xb3\xcc\xc8\xeb\xbf\xda\xa1\xa3\n    wload(function () {\n\n        try {\n\n            var need_restore = "1" == "1"; // \xca\xc7\xb7\xf1\xd7\xdf\xbb\xd6\xb8\xb4\xc9\xed\xb7\xdd\xc1\xf7\xb3\xcc\xa1\xa3\n\n            // \xc8\xe7\xb9\xfb\xd0\xe8\xd2\xaa\xd7\xdf\xbb\xd6\xb8\xb4\xc9\xed\xb7\xdd\xc1\xf7\xb3\xcc\xa3\xac\xb3\xa2\xca\xd4\xb4\xd3 cookie \xbb\xf1\xc8\xa1\xd3\xc3\xbb\xa7\xc9\xed\xb7\xdd\xa1\xa3\n            if (!need_restore || !Store.CookieHelper.get("SRF")) {\n\n                // \xc8\xf4\xbb\xf1\xc8\xa1\xca\xa7\xb0\xdc\xd7\xdf\xb4\xb4\xbd\xa8\xb7\xc3\xbf\xcd\xc1\xf7\xb3\xcc\xa1\xa3\n                // \xc1\xf7\xb3\xcc\xd6\xb4\xd0\xd0\xca\xb1\xbc\xe4\xb9\xfd\xb3\xa4\xa3\xa8\xb3\xac\xb9\xfd 3s\xa3\xa9\xa3\xac\xd4\xf2\xc8\xcf\xce\xaa\xb3\xf6\xb4\xed\xa1\xa3\n                var error_timeout = window.setTimeout("error_back()", 5000);\n\n                tid.get(function (tid, where, confidence) {\n                    // \xc8\xa1\xd6\xb8\xce\xc6\xcb\xb3\xc0\xfb\xcd\xea\xb3\xc9\xa3\xac\xc7\xe5\xb3\xfd\xb3\xf6\xb4\xed timeout \xa1\xa3\n                    window.clearTimeout(error_timeout);\n                    incarnate(tid, where, confidence);\n                });\n            } else {\n                // \xd3\xc3\xbb\xa7\xc9\xed\xb7\xdd\xb4\xe6\xd4\xda\xa3\xac\xb3\xa2\xca\xd4\xbb\xd6\xb8\xb4\xd3\xc3\xbb\xa7\xc9\xed\xb7\xdd\xa1\xa3\n                restore();\n            }\n        } catch (e) {\n            // \xb3\xf6\xb4\xed\xa1\xa3\n            error_back();\n        }\n    });\n\n    // \xa1\xb0\xb7\xb5\xbb\xd8\xa1\xb1 \xbb\xd8\xb5\xf7\xba\xaf\xca\xfd\xa1\xa3\n    var return_back = function (response) {\n\n        if (response["retcode"] == 20000000) {\n            back();\n        } else {\n            // \xb3\xf6\xb4\xed\xa1\xa3\n            error_back(response["msg"]);\n        }\n    };\n\n    // \xcc\xf8\xd7\xaa\xbb\xd8\xb3\xf5\xca\xbc\xb5\xd8\xd6\xb7\xa1\xa3\n    var back = function() {\n\n        var url = "https://weibo.com/";\n        if (url != "none") {\n            window.location.href = url;\n        }\n    };\n\n    // \xbf\xe7\xd3\xf2\xb9\xe3\xb2\xa5\xa1\xa3\n    var cross_domain = function (response) {\n\n        var from = "weibo";\n        var entry = "miniblog";\n        if (response["retcode"] == 20000000) {\n\n            var crossdomain_host = "login.sina.com.cn";\n            if (crossdomain_host != "none") {\n\n                var cross_domain_intr = window.location.protocol + "//" + crossdomain_host + "/visitor/visitor?a=crossdomain&cb=return_back&s=" +\n                        encodeURIComponent(response["data"]["sub"]) + "&sp=" + encodeURIComponent(response["data"]["subp"]) + "&from=" + from + "&_rand=" + Math.random() + "&entry=" + entry;\n                url.l(cross_domain_intr);\n            } else {\n\n                back();\n            }\n        } else {\n\n            // \xb3\xf6\xb4\xed\xa1\xa3\n            error_back(response["msg"]);\n        }\n    };\n\n    // \xce\xaa\xd3\xc3\xbb\xa7\xb8\xb3\xd3\xe8\xb7\xc3\xbf\xcd\xc9\xed\xb7\xdd \xa1\xa3\n    var incarnate = function (tid, where, conficence) {\n\n        var gen_conf = "";\n        var from = "weibo";\n        var incarnate_intr = window.location.protocol + "//" + window.location.host + "/visitor/visitor?a=incarnate&t=" +\n                encodeURIComponent(tid) + "&w=" + encodeURIComponent(where) + "&c=" + encodeURIComponent(conficence) +\n                "&gc=" + encodeURIComponent(gen_conf) + "&cb=cross_domain&from=" + from + "&_rand=" + Math.random();\n        url.l(incarnate_intr);\n    };\n\n    // \xbb\xd6\xb8\xb4\xd3\xc3\xbb\xa7\xb6\xaa\xca\xa7\xb5\xc4\xc9\xed\xb7\xdd\xa1\xa3\n    var restore = function () {\n\n        var from = "weibo";\n        var restore_intr = window.location.protocol + "//" + window.location.host +\n                "/visitor/visitor?a=restore&cb=restore_back&from=" + from + "&_rand=" + Math.random();\n\n        url.l(restore_intr);\n    };\n\n    // \xbf\xe7\xd3\xf2\xbb\xd6\xb8\xb4\xb6\xaa\xca\xa7\xb5\xc4\xc9\xed\xb7\xdd\xa1\xa3\n    var restore_back = function (response) {\n\n        // \xc9\xed\xb7\xdd\xbb\xd6\xb8\xb4\xb3\xc9\xb9\xa6\xd7\xdf\xb9\xe3\xb2\xa5\xc1\xf7\xb3\xcc\xa3\xac\xb7\xf1\xd4\xf2\xd7\xdf\xb4\xb4\xbd\xa8\xb7\xc3\xbf\xcd\xc1\xf7\xb3\xcc\xa1\xa3\n        if (response["retcode"] == 20000000) {\n\n            var url = "https://weibo.com/";\n            var alt = response["data"]["alt"];\n            var savestate = response["data"]["savestate"];\n            if (alt != "") {\n                requrl = (url == "none") ? "" : "&url=" + encodeURIComponent(url);\n                var params = "entry=sso&alt=" + encodeURIComponent(alt) + "&returntype=META" +\n                    "&gateway=1&savestate=" + encodeURIComponent(savestate) + requrl;\n                window.location.href = "https://login.sina.com.cn/sso/login.php?" + params;\n            } else {\n\n                cross_domain(response);\n            }\n        } else if(response[\'retcode\'] == 50111261 && isInIframe()) {\n            //do nothing\n        } else {\n\n            tid.get(function (tid, where, confidence) {\n                incarnate(tid, where, confidence);\n            });\n        }\n    };\n\n    // \xb3\xf6\xb4\xed\xc7\xe9\xbf\xf6\xb7\xb5\xbb\xd8\xb5\xc7\xc2\xbc\xd2\xb3\xa1\xa3\n    var error_back = function (msg) {\n\n        var url = "https://weibo.com/";\n        var clientType = "pc";\n        if (url != "none") {\n\n            if (url.indexOf("ssovie4c55=0") === -1) {\n                url += (((url.indexOf("?") === -1) ? "?" : "&") + "ssovie4c55=0");\n            }\n            if (clientType == "mobile") {\n            \twindow.location.href = "https://passport.weibo.cn/signin/login?r="+url;\n            } else{\n            \twindow.location.href = "https://weibo.com/login.php";\n            }\n        } else {\n\n            if(document.getElementById("message")) {\n                document.getElementById("message").innerHTML = "Error occurred" + (msg ? (": " + msg) : ".");\n            }\n        }\n    };\n\n    var isInIframe = function () {\n        try {\n            return window.self !== window.top;\n        } catch (e) {\n            return true;\n        }\n    };\n\n</script>\n</body>\n</html>'