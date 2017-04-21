/**
 * Created by WangJun on 2017/4/19.
 */
/**
  *定义：用例编辑的js类函数
  * vp:hsg
  * create date:2015-09
  * http://blog.csdn.net/hsg77
  */
//替换函数
$.format = function (source, params) {
    if (arguments.length == 1) return function () {
        var args = $.makeArray(arguments);
        args.unshift(source);
        return $.format.apply(this, args);
        };
    if (arguments.length > 2 && params.constructor != Array) {
        params = $.makeArray(arguments).slice(1);
        }
    if (params.constructor != Array) {
        params = [params];
    }
    $.each(params, function (i, n) {
    source = source.replace(new RegExp("\\{" + i + "\\}", "g"), n);
    });
    return source;
    };

//定义抽象类 基类-项目信息对象模型
; (function () {
    //
    $.ProjectElement = function () {
        //var e = $('#' + e_name);
        //默认属性值
        var m_ProName = '';
        var m_creater = '';
        var m_Suites = new Array();
        var m_tester = new Array();
        //属性的获取与设置方法
        this.m_ProName=function () {
            return m_ProName;
        };
        this.m_creater=function () {
            return m_creater;
        };
        this.m_Suites=function () {
            return m_Suites;
        };
        this.m_tester=function () {
            return m_tester;
        };
        this.set_ProName=function (value) {
            m_ProName=value;
        };
        this.set_creater=function (value) {
            m_creater=value;
        };
        this.set_Suites=function (value) {
            m_Suites=value;
        };
        this.set_tester=function (value) {
            m_tester=value;
        };
        this.insert_Suite=function (value) {
            m_Suites.push(value)
        };
        this.insert_tester=function (value) {
            m_tester.push(value)
        };
        return this;
    };
})(jQuery);
//定义抽象类 基类-项目信息-套件节点对象模型;
(function () {
    //
    $.SuiteTreeNodeElement = function () {
        //var e = $('#' + e_name);
        //默认属性值
        var m_SuiteName = '';
        var m_Cases=new Array();
        var m_tester = '';
        //属性的获取与设置方法
        this.m_SuiteName=function () {
            return m_SuiteName;
        };
        this.m_Cases=function () {
            return m_Cases;
        };
        this.m_tester=function () {
            return m_tester;
        };
        this.set_SuiteName=function (value) {
            m_SuiteName=value;
        };
        this.set_Cases=function (value) {
            m_Cases=value;
        };
        this.set_tester=function (value) {
            m_tester=value;
        };
        this.insert_Case=function (value) {
            m_Cases.push(value)
        };
        return this;
    };
})(jQuery);
//定义抽象类 基类-项目信息-用例节点对象模型;
(function () {
    //
    $.CaseTreeNodeElement = function () {
        //var e = $('#' + e_name);
        //默认属性值
        var m_CaseName = '';
        var m_CaseDataID='';
        var m_tester = '';
        //属性的获取与设置方法
        this.m_CaseName=function () {
            return m_CaseName;
        };
        this.m_CaseDataID=function () {
            return m_CaseDataID;
        };
        this.m_tester=function () {
            return m_tester;
        };
        this.set_CaseName=function (value) {
            m_CaseName=value;
        };
        this.set_tester=function (value) {
            m_tester=value;
        };
        return this;
    };
})(jQuery);
//定义生成项目树类
(function () {
    //
    $.CreateProjectTreeElement = function () {
        //var e = $('#' + e_name);
        //默认属性值
        var m_Projects= new Array();
        var m_ProjectTrees=new Array();
        var projNodeName='proj';
        var suiteNodeName='proj-suite'
        var caseNodeName='proj-suite-case'
        var dataNodeName='proj-suite-case-D'
        var nodeHtml='<ul class="{0}">{1}</ul>';
        var m_ProjectNodeHtml ='<li class="proj{0}">'+
                '<input type="checkbox" class="proj{0}-{0}" /><a class="proj{0}-{0}">{1}</a>'+
                '{2}'+
            '</li>';
        var m_SuiteNodeHtml='<li class="proj{0}-s{1}">'+
                        '<input type="checkbox" class="proj{0}-s{1}-{1}" /><a class="proj{0}-s{1}-{1}">{2}</a>'+
                            '{3}'+
                    '</li>';
        var m_CaseNodeHtml= '<li class="proj{0}-s{1}-c{2}">'+
                                '<input type="checkbox" class="proj{0}-s{1}-c{2}-{2}" /><a class="proj{0}-s{1}-c{2}-{2}">{3}</a>'+
                                '{4}'+
                            '</li>'
        var m_CaseDataHtml='<li class="proj{0}-s{1}-c{2}-d{3}"><input type="checkbox" class="proj{0}-s{1}-c{2}-d{3}-{3}" /><a class="proj{0}-s{1}-c{2}-d{3}-{3}">{4}</a></li>'
        var m_treeHtml='';
        //属性的获取与设置方法
        this.m_Projects=function () {
            return m_Projects;
        };
        this.m_ProjectTrees=function () {
            return m_ProjectTrees;
        };
        this.m_treeHtml=function () {
            return m_treeHtml;
        };
        this.m_tester=function () {
            return m_tester;
        };
        this.set_Projects=function (value) {
            m_Projects=value;
        };
        this.set_ProjectTrees=function (value) {
            m_ProjectTrees=value;
        };
        this.insert_Project=function (value) {
            m_Projects.push(value)
        };
        this.insert_ProjectTree=function (value) {
            m_ProjectTrees.push(value)
        };
        this.build_treeHtml=function () {
            var i=0,j=0,k=0;
            var TempProjsHtml='';
            for(i=0;i<m_Projects.length;i++){
                var TempSuitsHtmls='';
                for(j=0;j<m_Projects[i].m_Suites().length;j++){
                    var TempCasesHtml='';
                    for(k=0;k<m_Projects[i].m_Suites()[j].m_Cases().length;k++){
                        var TempCaseDataHtml='';
                        if (m_Projects[i].m_Suites()[j].m_Cases()[k].m_CaseDataID()){
                        TempCaseDataHtml=$.format(nodeHtml,dataNodeName,m_CaseDataHtml.format(i+1,j+1,k+1,k+1,m_ProjectTrees[i].m_Projects.m_Suites()[j].m_Cases()[k].m_CaseDataID()));
                        }
                        TempCasesHtml+=$.format(m_CaseNodeHtml,i+1,j+1,k+1,m_Projects[i].m_Suites()[j].m_Cases()[k].m_CaseName(),TempCaseDataHtml);
                    }
                    TempCasesHtml=$.format(nodeHtml,caseNodeName,TempCasesHtml);
                    TempSuitsHtmls+=$.format(m_SuiteNodeHtml,i+1,j+1,m_Projects[i].m_Suites()[j].m_SuiteName(),TempCasesHtml);
                }
                TempSuitsHtmls= $.format(nodeHtml,suiteNodeName,TempSuitsHtmls);
                if (TempSuitsHtmls)
                TempProjsHtml+=$.format(m_ProjectNodeHtml,i+1,m_Projects[i].m_ProName(),TempSuitsHtmls);
            }
            m_treeHtml=$.format(nodeHtml,projNodeName,TempProjsHtml);
        };
        return this;
    };
})(jQuery);
//定义抽象类 基类-项目列表对象转换;
(function () {
    //
    $.initTreeDataElement = function () {
        //var e = $('#' + e_name);
        //默认属性值
        var m_Projects = new Array();
        //属性的获取与设置方法
        this.m_Projects=function () {
            return m_Projects;
        };
        this.convent_ProjList=function (jsonDataArrag) {
            var projJsonArragData=jsonDataArrag;
            //eval(jsonDataArrag);
            for(var i=0;i<projJsonArragData.length;i++){
                var projectObj=new $.ProjectElement();
                for(var j=0;j<projJsonArragData[i].suite.length;j++){
                    var suiteOject=new $.SuiteTreeNodeElement();
                    for(var k=0;k<projJsonArragData[i].suite[j].case.length;k++){
                        var caseOject=new $.CaseTreeNodeElement();
                        caseOject.set_CaseName(projJsonArragData[i].suite[j].case[k].caseName)
                        suiteOject.insert_Case(caseOject)
                    }
                    suiteOject.set_SuiteName(projJsonArragData[i].suite[j].suiteName);
                    suiteOject.set_tester(projJsonArragData[i].suite[j].tester);
                    projectObj.insert_Suite(suiteOject);
                }
                projectObj.set_tester(projJsonArragData[i].tester);
                projectObj.set_ProName(projJsonArragData[i].projectName);
                projectObj.set_creater(projJsonArragData[i].creator);
                m_Projects.push(projectObj);
            }

        };
        return this;
    };
})(jQuery);


var aaa=[{
  "projectName" : "FastMap采集端安卓集成测试项目",
  "creator" : "wangjun",
  "tester" : ["wangjun"],
  "suite" : [{
      "case" : [{
          "caseName" : "POI新增模块调用测试"
        }, {
          "caseName" : "POI修改模块调用测试"
        }, {
          "caseName" : "POI删除模块调用测试"
        }, {
          "caseName" : "POI同一关系模块调用测试"
        }],
      "suiteName" : "POI制作模块集成测试套件",
      "tester" : "wangjun"
    }, {
      "case" : [{
          "caseName" : "Tips新增模块调用测试"
        }, {
          "caseName" : "Tips修改模块调用测试"
        }, {
          "caseName" : "Tips删除模块调用测试"
        }, {
          "caseName" : "Tips卡车交限模块调用测试"
        }, {
          "caseName" : "Tips条件限速模块调用测试"
        }, {
          "caseName" : "Tips卡车限制模块调用测试"
        }, {
          "caseName" : "Tips车道变化点模块调用测试"
        }, {
          "caseName" : "Tips可逆车道模块调用测试"
        }, {
          "caseName" : "Tips路口语音引导模块调用测试"
        }, {
          "caseName" : "Tips公交车道模块调用测试"
        }, {
          "caseName" : "Tips可变导向车道模块调用测试"
        }, {
          "caseName" : "Tips里程桩模块调用测试"
        }, {
          "caseName" : "Tips草图模块调用测试"
        }, {
          "caseName" : "Tips删除标记模块调用测试"
        }, {
          "caseName" : "Tips万能标记模块调用测试"
        }],
      "suiteName" : "Tips制作模块集成测试套件",
      "tester" : "wangjun"
    }, {
      "case" : [{
          "caseName" : "电子眼-SD020模块类内集成SD020001001接口"
        }, {
          "caseName" : "电子眼-SD020模块类内集成SD020001002接口"
        }, {
          "caseName" : "电子眼-SD020模块模块间集成SD004模块"
        }, {
          "caseName" : "电子眼-SD004模块模块间集成SD020模块"
        }, {
          "caseName" : "卡车限制-SD021模块类内集成SD021001001接口"
        }, {
          "caseName" : "卡车限制-SD021模块类内集成SD021001002接口"
        }, {
          "caseName" : "卡车限制-SD021模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车限制-SD004模块模块间集成SD021模块"
        }, {
          "caseName" : "卡车限速-SD025模块类内集成SD025001001接口"
        }, {
          "caseName" : "卡车限速-SD025模块类内集成SD025001002接口"
        }, {
          "caseName" : "卡车限速-SD025模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车限速-SD004模块模块间集成SD025模块"
        }, {
          "caseName" : "车道变化点-SD026模块类内集成SD026001001接口"
        }, {
          "caseName" : "车道变化点-SD026模块类内集成SD026001002接口"
        }, {          "caseName" : "车道变化点-SD026模块模块间集成SD004模块"

        }, {
          "caseName" : "车道变化点-SD004模块模块间集成SD026模块"
        }, {
          "caseName" : "可逆车道-SD031模块类内集成SD031001001接口"
        }, {
          "caseName" : "可逆车道-SD031模块类内集成SD031001002接口"
        }, {
          "caseName" : "可逆车道-SD031模块模块间集成SD004模块"
        }, {
          "caseName" : "可逆车道-SD004模块模块间集成SD031模块"
        }, {
          "caseName" : "卡车交限-SD038模块类内集成SD038001001接口"
        }, {
          "caseName" : "卡车交限-SD038模块类内集成SD038001002接口"
        }, {
          "caseName" : "卡车交限-SD038模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车交限-SD004模块模块间集成SD038模块"
        }, {
          "caseName" : "路口语音引导-SD041模块类内集成SD041001001接口"
        }, {
          "caseName" : "路口语音引导-SD041模块类内集成SD041001002接口"
        }, {
          "caseName" : "路口语音引导-SD041模块模块间集成SD004模块"
        }, {
          "caseName" : "路口语音引导-SD004模块模块间集成SD041模块"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001001接口"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001002接口"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块模块间集成SD004模块"
        }, {
          "caseName" : "禁止卡车驶入-SD004模块模块间集成SD043模块"
        }, {
          "caseName" : "公交车道-SD044模块类内集成SD044001001接口"
        }, {
          "caseName" : "公交车道-SD044模块类内集成SD044001002接口"
        }, {
          "caseName" : "公交车道-SD044模块模块间集成SD004模块"
        }, {
          "caseName" : "公交车道-SD004模块模块间集成SD044模块"
        }, {
          "caseName" : "可变导向车道-SD045模块类内集成SD045001001接口"
        }, {
          "caseName" : "可变导向车道-SD045模块类内集成SD045001002接口"
        }, {
          "caseName" : "可变导向车道-SD045模块模块间集成SD004模块"
        }, {
          "caseName" : "可变导向车道-SD004模块模块间集成SD045模块"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001001接口"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001002接口"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块模块间集成SD004模块"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD004模块模块间集成SD056模块"
        }, {
          "caseName" : "草图-SD059模块类内集成SD059001001接口"
        }, {
          "caseName" : "草图-SD059模块类内集成SD059001002接口"
        }, {
          "caseName" : "草图-SD059模块模块间集成SD004模块"
        }, {
          "caseName" : "草图-SD004模块模块间集成SD059模块"
        }, {
          "caseName" : "删除标记-SD061模块类内集成SD061001001接口"
        }, {
          "caseName" : "删除标记-SD061模块类内集成SD061001002接口"
        }, {
          "caseName" : "删除标记-SD061模块模块间集成SD004模块"
        }, {
          "caseName" : "删除标记-SD004模块模块间集成SD061模块"
        }, {
          "caseName" : "万能标记-SD062模块类内集成SD062001001接口"
        }, {
          "caseName" : "万能标记-SD062模块类内集成SD062001002接口"
        }, {
          "caseName" : "万能标记-SD062模块模块间集成SD004模块"
        }, {
          "caseName" : "万能标记-SD004模块模块间集成SD062模块"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012002-同一关系点击事件"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-获同一关系位置"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-寻找同一关系"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012003-过滤不可做同一关系的poi"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-可做同一关系分类"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-寻找可以做同一关系的kindcode列表"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012003-过滤不可做同一关系的poi"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系-"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD003集成SD012-同一关系点击事件"
        }],
      "suiteName" : "第七迭代变更模块集成测试套件",
      "tester" : "wangjun"
    }]
},{
  "projectName" : "FastMap采集端安卓集成测试项目",
  "creator" : "wangjun",
  "tester" : ["wangjun"],
  "suite" : [{
      "case" : [{
          "caseName" : "POI新增模块调用测试"
        }, {
          "caseName" : "POI修改模块调用测试"
        }, {
          "caseName" : "POI删除模块调用测试"
        }, {
          "caseName" : "POI同一关系模块调用测试"
        }],
      "suiteName" : "POI制作模块集成测试套件",
      "tester" : "wangjun"
    }, {
      "case" : [{
          "caseName" : "Tips新增模块调用测试"
        }, {
          "caseName" : "Tips修改模块调用测试"
        }, {
          "caseName" : "Tips删除模块调用测试"
        }, {
          "caseName" : "Tips卡车交限模块调用测试"
        }, {
          "caseName" : "Tips条件限速模块调用测试"
        }, {
          "caseName" : "Tips卡车限制模块调用测试"
        }, {
          "caseName" : "Tips车道变化点模块调用测试"
        }, {
          "caseName" : "Tips可逆车道模块调用测试"
        }, {
          "caseName" : "Tips路口语音引导模块调用测试"
        }, {
          "caseName" : "Tips公交车道模块调用测试"
        }, {
          "caseName" : "Tips可变导向车道模块调用测试"
        }, {
          "caseName" : "Tips里程桩模块调用测试"
        }, {
          "caseName" : "Tips草图模块调用测试"
        }, {
          "caseName" : "Tips删除标记模块调用测试"
        }, {
          "caseName" : "Tips万能标记模块调用测试"
        }],
      "suiteName" : "Tips制作模块集成测试套件",
      "tester" : "wangjun"
    }, {
      "case" : [{
          "caseName" : "电子眼-SD020模块类内集成SD020001001接口"
        }, {
          "caseName" : "电子眼-SD020模块类内集成SD020001002接口"
        }, {
          "caseName" : "电子眼-SD020模块模块间集成SD004模块"
        }, {
          "caseName" : "电子眼-SD004模块模块间集成SD020模块"
        }, {
          "caseName" : "卡车限制-SD021模块类内集成SD021001001接口"
        }, {
          "caseName" : "卡车限制-SD021模块类内集成SD021001002接口"
        }, {
          "caseName" : "卡车限制-SD021模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车限制-SD004模块模块间集成SD021模块"
        }, {
          "caseName" : "卡车限速-SD025模块类内集成SD025001001接口"
        }, {
          "caseName" : "卡车限速-SD025模块类内集成SD025001002接口"
        }, {
          "caseName" : "卡车限速-SD025模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车限速-SD004模块模块间集成SD025模块"
        }, {
          "caseName" : "车道变化点-SD026模块类内集成SD026001001接口"
        }, {
          "caseName" : "车道变化点-SD026模块类内集成SD026001002接口"
        }, {          "caseName" : "车道变化点-SD026模块模块间集成SD004模块"

        }, {
          "caseName" : "车道变化点-SD004模块模块间集成SD026模块"
        }, {
          "caseName" : "可逆车道-SD031模块类内集成SD031001001接口"
        }, {
          "caseName" : "可逆车道-SD031模块类内集成SD031001002接口"
        }, {
          "caseName" : "可逆车道-SD031模块模块间集成SD004模块"
        }, {
          "caseName" : "可逆车道-SD004模块模块间集成SD031模块"
        }, {
          "caseName" : "卡车交限-SD038模块类内集成SD038001001接口"
        }, {
          "caseName" : "卡车交限-SD038模块类内集成SD038001002接口"
        }, {
          "caseName" : "卡车交限-SD038模块模块间集成SD004模块"
        }, {
          "caseName" : "卡车交限-SD004模块模块间集成SD038模块"
        }, {
          "caseName" : "路口语音引导-SD041模块类内集成SD041001001接口"
        }, {
          "caseName" : "路口语音引导-SD041模块类内集成SD041001002接口"
        }, {
          "caseName" : "路口语音引导-SD041模块模块间集成SD004模块"
        }, {
          "caseName" : "路口语音引导-SD004模块模块间集成SD041模块"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001001接口"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001002接口"
        }, {
          "caseName" : "禁止卡车驶入-SD043模块模块间集成SD004模块"
        }, {
          "caseName" : "禁止卡车驶入-SD004模块模块间集成SD043模块"
        }, {
          "caseName" : "公交车道-SD044模块类内集成SD044001001接口"
        }, {
          "caseName" : "公交车道-SD044模块类内集成SD044001002接口"
        }, {
          "caseName" : "公交车道-SD044模块模块间集成SD004模块"
        }, {
          "caseName" : "公交车道-SD004模块模块间集成SD044模块"
        }, {
          "caseName" : "可变导向车道-SD045模块类内集成SD045001001接口"
        }, {
          "caseName" : "可变导向车道-SD045模块类内集成SD045001002接口"
        }, {
          "caseName" : "可变导向车道-SD045模块模块间集成SD004模块"
        }, {
          "caseName" : "可变导向车道-SD004模块模块间集成SD045模块"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001001接口"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001002接口"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD056模块模块间集成SD004模块"
        }, {
          "caseName" : "打点模块新增里程桩功能-SD004模块模块间集成SD056模块"
        }, {
          "caseName" : "草图-SD059模块类内集成SD059001001接口"
        }, {
          "caseName" : "草图-SD059模块类内集成SD059001002接口"
        }, {
          "caseName" : "草图-SD059模块模块间集成SD004模块"
        }, {
          "caseName" : "草图-SD004模块模块间集成SD059模块"
        }, {
          "caseName" : "删除标记-SD061模块类内集成SD061001001接口"
        }, {
          "caseName" : "删除标记-SD061模块类内集成SD061001002接口"
        }, {
          "caseName" : "删除标记-SD061模块模块间集成SD004模块"
        }, {
          "caseName" : "删除标记-SD004模块模块间集成SD061模块"
        }, {
          "caseName" : "万能标记-SD062模块类内集成SD062001001接口"
        }, {
          "caseName" : "万能标记-SD062模块类内集成SD062001002接口"
        }, {
          "caseName" : "万能标记-SD062模块模块间集成SD004模块"
        }, {
          "caseName" : "万能标记-SD004模块模块间集成SD062模块"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012002-同一关系点击事件"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-获同一关系位置"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-寻找同一关系"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012003-过滤不可做同一关系的poi"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-可做同一关系分类"
        }, {
          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-寻找可以做同一关系的kindcode列表"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012003-过滤不可做同一关系的poi"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系-"
        }, {
          "caseName" : "同一关系-SD012模块内类间集成SD003集成SD012-同一关系点击事件"
        }],
      "suiteName" : "第七迭代变更模块集成测试套件",
      "tester" : "wangjun"
    }]
}]
var aaaa='[{"projectName" : "FastMap采集端安卓集成测试项目",'+
'  "creator" : "wangjun",'+
'  "tester" : ["wangjun"],'+
'  "suite" : [{'+
'      "case" : [{'+
'          "caseName" : "POI新增模块调用测试"'+
'        }, {'+
'          "caseName" : "POI修改模块调用测试"'+
'        }, {'+
'          "caseName" : "POI删除模块调用测试"'+
'        }, {'+
'          "caseName" : "POI同一关系模块调用测试"'+
'        }],'+
'      "suiteName" : "POI制作模块集成测试套件",'+
'      "tester" : "wangjun"'+
'    }, {'+
'      "case" : [{'+
'          "caseName" : "Tips新增模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips修改模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips删除模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips卡车交限模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips条件限速模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips卡车限制模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips车道变化点模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips可逆车道模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips路口语音引导模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips公交车道模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips可变导向车道模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips里程桩模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips草图模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips删除标记模块调用测试"'+
'        }, {'+
'          "caseName" : "Tips万能标记模块调用测试"'+
'        }],'+
'      "suiteName" : "Tips制作模块集成测试套件",'+
'      "tester" : "wangjun"'+
'    }, {'+
'      "case" : [{'+
'          "caseName" : "电子眼-SD020模块类内集成SD020001001接口"'+
'        }, {'+
'          "caseName" : "电子眼-SD020模块类内集成SD020001002接口"'+
'        }, {'+
'          "caseName" : "电子眼-SD020模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "电子眼-SD004模块模块间集成SD020模块"'+
'        }, {'+
'          "caseName" : "卡车限制-SD021模块类内集成SD021001001接口"'+
'        }, {'+
'          "caseName" : "卡车限制-SD021模块类内集成SD021001002接口"'+
'        }, {'+
'          "caseName" : "卡车限制-SD021模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "卡车限制-SD004模块模块间集成SD021模块"'+
'        }, {'+
'          "caseName" : "卡车限速-SD025模块类内集成SD025001001接口"'+
'        }, {'+
'          "caseName" : "卡车限速-SD025模块类内集成SD025001002接口"'+
'        }, {'+
'          "caseName" : "卡车限速-SD025模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "卡车限速-SD004模块模块间集成SD025模块"'+
'        }, {'+
'          "caseName" : "车道变化点-SD026模块类内集成SD026001001接口"'+
'        }, {'+
'          "caseName" : "车道变化点-SD026模块类内集成SD026001002接口"'+
'        }, {          "caseName" : "车道变化点-SD026模块模块间集成SD004模块"'+
''+
'        }, {'+
'          "caseName" : "车道变化点-SD004模块模块间集成SD026模块"'+
'        }, {'+
'          "caseName" : "可逆车道-SD031模块类内集成SD031001001接口"'+
'        }, {'+
'          "caseName" : "可逆车道-SD031模块类内集成SD031001002接口"'+
'        }, {'+
'          "caseName" : "可逆车道-SD031模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "可逆车道-SD004模块模块间集成SD031模块"'+
'        }, {'+
'          "caseName" : "卡车交限-SD038模块类内集成SD038001001接口"'+
'        }, {'+
'          "caseName" : "卡车交限-SD038模块类内集成SD038001002接口"'+
'        }, {'+
'          "caseName" : "卡车交限-SD038模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "卡车交限-SD004模块模块间集成SD038模块"'+
'        }, {'+
'          "caseName" : "路口语音引导-SD041模块类内集成SD041001001接口"'+
'        }, {'+
'          "caseName" : "路口语音引导-SD041模块类内集成SD041001002接口"'+
'        }, {'+
'          "caseName" : "路口语音引导-SD041模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "路口语音引导-SD004模块模块间集成SD041模块"'+
'        }, {'+
'          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001001接口"'+
'        }, {'+
'          "caseName" : "禁止卡车驶入-SD043模块类内集成SD043001002接口"'+
'        }, {'+
'          "caseName" : "禁止卡车驶入-SD043模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "禁止卡车驶入-SD004模块模块间集成SD043模块"'+
'        }, {'+
'          "caseName" : "公交车道-SD044模块类内集成SD044001001接口"'+
'        }, {'+
'          "caseName" : "公交车道-SD044模块类内集成SD044001002接口"'+
'        }, {'+
'          "caseName" : "公交车道-SD044模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "公交车道-SD004模块模块间集成SD044模块"'+
'        }, {'+
'          "caseName" : "可变导向车道-SD045模块类内集成SD045001001接口"'+
'        }, {'+
'          "caseName" : "可变导向车道-SD045模块类内集成SD045001002接口"'+
'        }, {'+
'          "caseName" : "可变导向车道-SD045模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "可变导向车道-SD004模块模块间集成SD045模块"'+
'        }, {'+
'          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001001接口"'+
'        }, {'+
'          "caseName" : "打点模块新增里程桩功能-SD056模块类内集成SD056001002接口"'+
'        }, {'+
'          "caseName" : "打点模块新增里程桩功能-SD056模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "打点模块新增里程桩功能-SD004模块模块间集成SD056模块"'+
'        }, {'+
'          "caseName" : "草图-SD059模块类内集成SD059001001接口"'+
'        }, {'+
'          "caseName" : "草图-SD059模块类内集成SD059001002接口"'+
'        }, {'+
'          "caseName" : "草图-SD059模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "草图-SD004模块模块间集成SD059模块"'+
'        }, {'+
'          "caseName" : "删除标记-SD061模块类内集成SD061001001接口"'+
'        }, {'+
'          "caseName" : "删除标记-SD061模块类内集成SD061001002接口"'+
'        }, {'+
'          "caseName" : "删除标记-SD061模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "删除标记-SD004模块模块间集成SD061模块"'+
'        }, {'+
'          "caseName" : "万能标记-SD062模块类内集成SD062001001接口"'+
'        }, {'+
'          "caseName" : "万能标记-SD062模块类内集成SD062001002接口"'+
'        }, {'+
'          "caseName" : "万能标记-SD062模块模块间集成SD004模块"'+
'        }, {'+
'          "caseName" : "万能标记-SD004模块模块间集成SD062模块"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012002-同一关系点击事件"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-获同一关系位置"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类内集成SD012001集成-寻找同一关系"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD012001集成SD012003-过滤不可做同一关系的poi"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-可做同一关系分类"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类内集成SD012003集成-寻找可以做同一关系的kindcode列表"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012003-过滤不可做同一关系的poi"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD012002集成SD012001-点击同一关系-"'+
'        }, {'+
'          "caseName" : "同一关系-SD012模块内类间集成SD003集成SD012-同一关系点击事件"'+
'        }],'+
'      "suiteName" : "第七迭代变更模块集成测试套件",'+
'      "tester" : "wangjun"'+
'    }, {'+
'      "suiteName" : "第八迭代变更模块集成测试套件",'+
'      "tester" : "wangjun"'+
'    }]';

$().ready(function () {
    var projectArragData=aaa;
    var projectsData=new $.initTreeDataElement();
    projectsData.convent_ProjList(projectArragData);
    var projectsTreeHtmlObject=new $.CreateProjectTreeElement();
    projectsTreeHtmlObject.set_Projects(projectsData.m_Projects());
    projectsTreeHtmlObject.build_treeHtml();
    var treeObject=$("#treeBox");
    //console.log(projectsTreeHtmlObject.m_treeHtml());
    treeObject.html(projectsTreeHtmlObject.m_treeHtml());
})