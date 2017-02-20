/**
 * Created by wangjun on 17/2/20.
 */
$("#startButton").click(function(){
    start();
})
$("#stopButton").click(function(){
    stop();
})
function start(){
    if (getCookie("HttpFlag")=="ed" || getCookie("HttpFlag")==null){
        $.ajax({
            type:"GET",
            url:UrlHeader+"/IdeaPartnerXServer/request_node/testStart/",
            data:{access_token:"00000193IZGEHZ03EC7EF15252EEF2256E27F0E90339B99C",OptName:$("#TestOptName").var(),OptDesc:$("#TestOptDesc").var()},
            async:false,
            cache:false,
            dataType:json,
            success:function(data){
                alert("开始操作吧")
            },
            error:function(){
                alert("偶哦!!出错了!!,请联系管理员吧!!")
            }
        })
        setCookie('HttpFlag','ing',1);
    }

    alert('2')
}


function stop(){
        if (getCookie("HttpFlag")=="ing"){
            $.ajax({
                type: "GET",
                url: UrlHeader + "/IdeaPartnerXServer/request_node/testStart/",
                data: {
                    access_token: getCookie("FM-app-USER-"),
                    OptName: $("#TestOptName").var(),
                    OptDesc: $("#TestOptDesc").var()
                },
                async: false,
                cache: false,
                dataType: json,
                success: function (data) {
                    alert("操作了")
                },
                error: function () {
                    alert("偶哦!!出错了!!,请联系管理员吧!!")
                }
            })
            setCookie('HttpFlag', 'ed', 1);
        }
        else
            alert("已经停止操作记录!!")
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
