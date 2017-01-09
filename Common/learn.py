#!/usr/bin/env python
# -*- coding: utf-8 -*
# 用于数据挖掘的公共方法
__author__ = 'wangjun'

# -*-coding:utf-8-*-
'''''
    朴素贝叶斯算法
'''




global className
className = "class"


def calc_class(train, classValue):
    # 计算分类的概率
    _num_cls = 0
    _num_trains = len(train)
    for t in train:
        if t[className] == classValue:
            print t[className]
            _num_cls += 1
    return  float(_num_cls)/float(_num_trains)

def calc_attr(train, classValue, attrName, attrValue):
    # 计算属性的概率
    _num_cls  = 0
    _num_attr = 0
    for a in train:
        if a[className] == classValue:
            _num_cls += 1
            if a[attrName] == attrValue:
                _num_attr += 1

    if _num_attr == 0:
        _num_attr = 1
    return float(_num_attr) / float(_num_cls)


def bayes(train, test, classY, classN):

    _prob_Y = calc_class(train, classY)
    _prob_N = calc_class(train, classN)
    print _prob_N
    print _prob_Y
    for key,value in test.items():
        _prob_Y *= calc_attr(train, classY, key, value)
        _prob_N *= calc_attr(train, classN, key, value)

    return {classY:_prob_Y,classN:_prob_N}



if __name__=='__main__':
    # 训练数据
    train = [
             {"outlook":"sunny",    "temp":"hot",  "humidity":"high",   "wind":"weak",   "class":"no" },
             {"outlook":"sunny",    "temp":"hot",  "humidity":"high",   "wind":"strong", "class":"no" },
             {"outlook":"overcast", "temp":"hot",  "humidity":"high",   "wind":"weak",   "class":"yes" },
             {"outlook":"rain",     "temp":"mild", "humidity":"high",   "wind":"weak",   "class":"yes" },
             {"outlook":"rain",     "temp":"cool", "humidity":"normal", "wind":"weak",   "class":"yes" },
             {"outlook":"rain",     "temp":"cool", "humidity":"normal", "wind":"strong", "class":"no" },
             {"outlook":"overcast", "temp":"cool", "humidity":"normal", "wind":"strong", "class":"yes" },
             {"outlook":"sunny",    "temp":"mild", "humidity":"high",   "wind":"weak",   "class":"no" },
             {"outlook":"sunny",    "temp":"cool", "humidity":"normal", "wind":"weak",   "class":"yes" },
             {"outlook":"rain",     "temp":"mild", "humidity":"normal", "wind":"weak",   "class":"yes" },
             {"outlook":"sunny",    "temp":"mild", "humidity":"normal", "wind":"strong", "class":"yes" },
             {"outlook":"overcast", "temp":"mild", "humidity":"high",   "wind":"strong", "class":"yes" },
             {"outlook":"overcast", "temp":"hot",  "humidity":"normal", "wind":"weak",   "class":"yes" },
             {"outlook":"rain",     "temp":"mild", "humidity":"high",   "wind":"strong", "class":"no" },
             ]
    # 测试数据
    test = {"outlook":"overcast","temp":"cool","humidity":"high","wind":"strong"}

    print bayes(train, test, "yes", "no")