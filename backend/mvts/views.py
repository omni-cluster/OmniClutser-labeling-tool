from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from mvts.models import *
import json
from django.core import serializers
from PROPATH import PATH
import os
import shutil
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

DATA = ''
RECONSTRUCT_DATA = ''


# 检查是否存在数据
def search_file(request):
    if request.method == 'GET':
        path_str = PATH + 'Data'
        if not os.path.exists(path_str):
            os.makedirs(path_str)
            return HttpResponse('Not Found')
        else:
            if os.path.exists(os.path.join(path_str, 'data.npy')):
                return HttpResponse('Existed')
    return HttpResponse('Not Found')


def clear_file(request):
    if request.method == 'GET':
        path_str = PATH + 'Data'
        shutil.copytree(path_str, path_str + 'backup')
        shutil.rmtree(path_str)
        os.makedirs(path_str)
        return HttpResponse('success')
    return HttpResponse('failed')


def read_save_file(request):
    if request.method == 'POST':
        file_path = request.POST.get('filePath', None)
        try:
            global DATA
            target_path = os.path.join(PATH, 'Data/data.npy')
            DATA = np.load(file_path)
            shutil.copy(file_path, target_path)
            return HttpResponse(DATA.shape[0])
        except Exception as e:
            print(e)
            return HttpResponse('failed')
    return HttpResponse('failed')


def read_file(request):
    if request.method == 'GET':
        try:
            global DATA
            target_path = os.path.join(PATH, 'Data/data.npy')
            DATA = np.load(target_path)
            return HttpResponse(DATA.shape[0])
        except Exception as e:
            print(e)
            return HttpResponse('failed')
    return HttpResponse('failed')


def read_data(request):
    if request.method == 'POST':
        data_index = int(request.POST.get('data_index', None))
        data = DATA[data_index - 1]
        data = data.tolist()
        return HttpResponse(json.dumps(data))
    return HttpResponse('failed')


def read_data_list(request):
    if request.method == 'POST':
        data_index = list(map(int, request.POST.getlist('data_index[]', [])))
        data_index = list(map(lambda x: x - 1, data_index))
        data_index = np.array(data_index)
        data = DATA[data_index].tolist()
        return HttpResponse(json.dumps(data))
    return HttpResponse('failed')


def read_label_list(request):
    if request.method == 'POST':
        old_label_path = PATH + 'Data/old_label.npy'
        old_label = np.load(old_label_path)
        data_index = list(map(int, request.POST.getlist('data_index[]', [])))
        data_index = list(map(lambda x: x - 1, data_index))
        data_index = np.array(data_index)
        data = old_label[data_index].tolist()
        return HttpResponse(json.dumps(data))
    return HttpResponse('failed')


# 读取label文件
def get_label(request):
    if request.method == 'GET':
        label_path = PATH + 'Data/label.txt'
        if os.path.exists(label_path):
            label = {}
            with open(label_path, 'r') as r:
                for l in r:
                    l = l.split(' : ')
                    if len(l) > 1:
                        label[int(l[0])] = int(l[1][:-1])
            return HttpResponse(json.dumps(label))
        else:
            return HttpResponse('no label data')
    return HttpResponse('failed')


# 读取template文件
def get_template(request):
    if request.method == 'GET':
        template_path = PATH + 'Data/template.txt'
        if os.path.exists(template_path):
            template = {}
            with open(template_path, 'r') as r:
                for l in r:
                    tem_list = []
                    l = l.split(' : ')
                    if len(l) > 1:
                        template[int(l[0])] = int(l[1])
            return HttpResponse(json.dumps(template))
        else:
            return HttpResponse('no template data')
    return HttpResponse('failed')


# 标注结果写入文件
def write_label(label, path):
    export_path = os.path.join(path, 'label.txt')
    try:
        with open(export_path, 'w') as w:
            if label:
                for k, v in label.items():
                    w.write(str(k) + ' : ' + str(v) + '\n')
        return True
    except Exception as e:
        print(e)
        return False
    return False


def write_template(template, path):
    template_path = PATH + 'Data/template.txt'
    export_path = os.path.join(path, 'template.txt')
    try:
        with open(template_path, 'w') as w:
            if template:
                for k, v in template.items():
                    w.write(str(k) + ' : ' + str(v) + '\n')
        with open(export_path, 'w') as w:
            if template:
                for k, v in template.items():
                    w.write(str(k) + ' : ' + str(v) + '\n')
        return True
    except Exception as e:
        print(e)
        return False
    return False


def export_data(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        label = post_data.get('label', None)
        template = post_data.get('template', None)
        path = post_data.get('path', None)
        path = eval(repr(path).replace('\\\\', '\\'))
        if write_template(template, path) and write_label(label, path):
            return HttpResponse('success')
    return HttpResponse('failed')


def read_z_list(request):
    if request.method == 'POST':
        z_path = PATH + 'Data/z.npy'
        z = np.load(z_path)
        data_index = list(map(int, request.POST.getlist('data_index[]', [])))
        data_index = list(map(lambda x: x - 1, data_index))
        data_index = np.array(data_index)
        data = z[data_index].tolist()
        return HttpResponse(json.dumps(data))
    return HttpResponse('failed')


def read_reconstruct_list(request):
    if request.method == 'POST':
        global RECONSTRUCT_DATA
        if RECONSTRUCT_DATA == '':
            reconstruct_data_path = PATH + 'Data/reconstruct.npy'
            RECONSTRUCT_DATA = np.load(reconstruct_data_path)
        data_index = list(map(int, request.POST.getlist('data_index[]', [])))
        data_index = list(map(lambda x: x - 1, data_index))
        data_index = np.array(data_index)
        data = RECONSTRUCT_DATA[data_index].tolist()
        return HttpResponse(json.dumps(data))
    return HttpResponse('failed')


def reload_reconstruct(request):
    if request.method == 'POST':
        global RECONSTRUCT_DATA
        reconstruct_data_path = PATH + 'Data/reconstruct.npy'
        RECONSTRUCT_DATA = np.load(reconstruct_data_path)

    return HttpResponse('true')
