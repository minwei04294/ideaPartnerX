/**
 * Created by wangjun on 17/2/20.
 */
//var UrlHeader="http://127.0.0.1:8000"
if (getCookie('TestOptName'))
    $("#TestOptName").val(getCookie('TestOptName'));
if (getCookie('TestOptDesc'))
    $("#TestOptDesc").val(getCookie('TestOptDesc'));
// if (getCookieToken()){
//     TokenValue=getCookieToken()
// }
// else
//     alert("未检测到你的浏览器中存在用户票据信息，你登录编辑平台了么！！");
$("#startButton").click(function(){
    start();
})
$("#stopButton").click(function(){
    stop();
})

function start() {
    if (getCookie("HttpFlag") == "ing" ) {

        alert("亲!!已经执行开始操作了!!")
    }
    else
        {
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
            setCookie('TestOptName',$("#TestOptName").val(),1);
            setCookie('TestOptDesc',$("#TestOptDesc").val(),1);
            setCookie('HttpFlag', 'ing', 1);
        } catch (e) {
            alert(e);
            }
        }
}

function stop(){

        if ($("#TestOptName").val()){
            OptNameValue=$("#TestOptName").val()
        }
        else
            OptNameValue=getCookie('TestOptName');
        if($("#TestOptDesc").val()){
            OptDescValue=$("#TestOptDesc").val()
        }
        else
            OptDescValue=getCookie('TestOptDesc');
        if (getCookie("HttpFlag")=="ing"){
            $.support.cors=true;
            $.ajax({
                type: "GET",
                url: UrlHeader + "/IdeaPartnerXServer/request_node/testStop/",
                data: {
                    access_token: TokenValue,
                    OptName: OptNameValue,
                    OptDesc: OptDescValue
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
            clearCookie('TestOptName');
            clearCookie('TestOptDesc');
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
//
// function getCookieToken(){
//     var token=""
//     document.cookie="name=value;domain=192.168.4.130";
//     var cookieList=""+document.cookie.split(";")
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
// }


