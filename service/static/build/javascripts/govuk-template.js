(function(){"use strict";var a=this;"undefined"==typeof a.GOVUK&&(a.GOVUK={}),GOVUK.cookie=function(a,b,c){return"undefined"!=typeof b?b===!1||null===b?GOVUK.setCookie(a,"",{days:-1}):GOVUK.setCookie(a,b,c):GOVUK.getCookie(a)},GOVUK.setCookie=function(a,b,c){"undefined"==typeof c&&(c={});var d=a+"="+b+"; path=/";if(c.days){var e=new Date;e.setTime(e.getTime()+24*c.days*60*60*1e3),d=d+"; expires="+e.toGMTString()}"https:"==document.location.protocol&&(d+="; Secure"),document.cookie=d},GOVUK.getCookie=function(a){for(var b=a+"=",c=document.cookie.split(";"),d=0,e=c.length;e>d;d++){for(var f=c[d];" "==f.charAt(0);)f=f.substring(1,f.length);if(0===f.indexOf(b))return decodeURIComponent(f.substring(b.length))}return null}}).call(this),function(){"use strict";var a=this;"undefined"==typeof a.GOVUK&&(a.GOVUK={}),GOVUK.addCookieMessage=function(){var a=document.getElementById("global-cookie-message"),b=a&&null===GOVUK.cookie("seen_cookie_message");b&&(a.style.display="block",GOVUK.cookie("seen_cookie_message","yes",{days:28}))}}.call(this),function(){"use strict";var a,b=null!==window.navigator.userAgent.match(/(\(Windows[\s\w\.]+\))[\/\(\s\w\.\,\)]+(Version\/[\d\.]+)\s(Safari\/[\d\.]+)/);if(b&&(a=document.createElement("style"),a.setAttribute("type","text/css"),a.setAttribute("media","print"),a.innerHTML='@font-face { font-family: nta !important; src: local("Arial") !important; }',document.getElementsByTagName("head")[0].appendChild(a)),window.GOVUK&&GOVUK.addCookieMessage&&GOVUK.addCookieMessage(),document.querySelectorAll&&document.addEventListener){var c,d,e=document.querySelectorAll(".js-header-toggle");for(c=0,d=e.length;d>c;c++)e[c].addEventListener("click",function(a){a.preventDefault();var b=document.getElementById(this.getAttribute("href").substr(1)),c=b.getAttribute("class")||"",d=this.getAttribute("class")||"";-1!==c.indexOf("js-visible")?b.setAttribute("class",c.replace(/(^|\s)js-visible(\s|$)/,"")):b.setAttribute("class",c+" js-visible"),-1!==d.indexOf("js-hidden")?this.setAttribute("class",d.replace(/(^|\s)js-hidden(\s|$)/,"")):this.setAttribute("class",d+" js-hidden")})}}.call(this);