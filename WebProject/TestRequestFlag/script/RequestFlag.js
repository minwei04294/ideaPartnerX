/**
 * Created by wangjun on 17/2/20.
 */
//var UrlHeader="http://127.0.0.1:8000"
$("#startButton").click(function(){
    start();
})
$("#stopButton").click(function(){
    stop();
})
function start() {
    if (getCookie("HttpFlag") == "ed" || getCookie("HttpFlag") == null) {
        try {
            $.support.cors = true;
            $.ajax({
                type: "GET",
                url: UrlHeader + "/IdeaPartnerXServer/request_node/testStart/",
                data: {
                    access_token: TokenValue,
                    OptName: $("#TestOptName").val(),
                    OptDesc: $("#TestOptDesc").val()
                },
                async: false,
                cache: false,
                dataType: "json",
                success: function (data) {
                    alert("开始操作吧")
                },
                error: function () {
                    alert("偶哦!!出错了!!,请联系管理员吧!!")
                }
            });
            setCookie('HttpFlag', 'ing', 1);
        } catch (e) {
            alert(e);
        }
    }
    else
        {
            alert("亲!!已经执行开始操作了!!")
        }
}

function stop(){
        if (getCookie("HttpFlag")=="ing"){
            $.support.cors=true;
            $.ajax({
                type: "GET",
                url: UrlHeader + "/IdeaPartnerXServer/request_node/testStop/",
                data: {
                    access_token: TokenValue,
                    OptName: $("#TestOptName").val(),
                    OptDesc: $("#TestOptDesc").val()
                },
                async: false,
                cache: false,
                dataType: "json",
                success: function (data) {
                    alert("操作停止了")
                },
                error: function () {
                    alert("偶哦!!出错了!!,请联系管理员吧!!")
                }
            });
            clearCookie('HttpFlag');
        }
        else
            alert("小朋友,已经停止操作记录!!");
}
function setCookie(c_name,value,expiredays){
    var  exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays)
    document.cookie=c_name+"="+value+((expiredays==null) ? "":";expires="+exdate.toDateString())
}
function getCookie(c_name){
    var arr,reg=new RegExp("(^|)"+c_name+"=([^;]*)(;|$)");
    if (arr=document.cookie.match(reg))
        return decodeURI(arr[2]);
    else
        return null;
}
function clearCookie(c_name){
    setCookie(c_name,"",-1)
}
//function getCookieToken(){
//    var token=""
//    var cookieList=""+document.cookie.split(";")
//    for(var i=0;i<cookieList.length;i++){
//        alert(cookieList[i])
//        if(cookieList[i].substring(0,12)=="FM-app-USER-"){
//           token=cookieList[i].substring(12,72)
//        }
//        if (token){
//            alert(token)
//            return token;
//            break;
//        }
//        else
//            //return '00000193IZGEHZ03EC7EF15252EEF2256E27F0E90339B99C';
//        return '';
//    }
//}


