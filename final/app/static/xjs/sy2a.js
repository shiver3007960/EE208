try {
    var s_BKb = function(a) {
        this.Qk = a
    };

} catch (e) {
    _DumpException(e)
}
try {
    var s_Am = function(a) {
        s_J.call(this, a.Ka);
        var b = this;
        this.window = a.service.window.get();
        this.wa = this.Qk();
        this.oa = window.orientation;
        this.ka = function() {
            var c = b.Qk()
              , d = b.Kib() && 90 === Math.abs(window.orientation) && b.oa === -1 * window.orientation;
            b.oa = window.orientation;
            if (c !== b.wa || d) {
                b.wa = c;
                d = s_e(b.Be);
                for (var e = d.next(); !e.done; e = d.next()) {
                    e = e.value;
                    var f = new s_BKb(c);
                    try {
                        e(f)
                    } catch (g) {
                        s_ca(g)
                    }
                }
            }
        }
        ;
        this.Be = new Set;
        this.window.addEventListener("resize", this.ka);
        this.Kib() && this.window.addEventListener("orientationchange", this.ka)
    };
    s_w(s_Am, s_J);
    s_Am.nb = s_J.nb;
    s_Am.Fa = function() {
        return {
            service: {
                window: s_oj
            }
        }
    }
    ;
    s_Am.prototype.addListener = function(a) {
        this.Be.add(a)
    }
    ;
    s_Am.prototype.removeListener = function(a) {
        this.Be.delete(a)
    }
    ;
    s_Am.prototype.Qk = function() {
        if (s_CKb()) {
            var a = s_Dh(this.window);
            a = new s_kh(a.width,Math.round(a.width * this.window.innerHeight / this.window.innerWidth))
        } else
            a = this.wc() || (s_na() ? s_CKb() : this.window.visualViewport) ? s_Dh(this.window) : new s_kh(this.window.innerWidth,this.window.innerHeight);
        return a.height < a.width
    }
    ;
    s_Am.prototype.destroy = function() {
        this.window.removeEventListener("resize", this.ka);
        this.window.removeEventListener("orientationchange", this.ka)
    }
    ;
    var s_CKb = function() {
        return s_na() && s_lf.mG() && !navigator.userAgent.includes("GSA")
    };
    s_Am.prototype.wc = function() {
        return s_DKb
    }
    ;
    s_Am.prototype.Kib = function() {
        return "orientation"in window
    }
    ;
    var s_DKb = !1;
    s_pj(s_JKa, s_Am);

    s_DKb = !0;

} catch (e) {
    _DumpException(e)
}
try {
    s_a("aLUfP");

    s_b();

} catch (e) {
    _DumpException(e)
}
// Google Inc.
