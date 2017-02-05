#-* coding: utf-8  *-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, render
from models import Friend
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User

@login_required
def showmap(request):
	showid = request.GET["id"]
	if len(Friend.objects.filter(id=showid, user=request.user)) > 0:
		return render_to_response("showmap.html", Context({"address": Friend.objects.get(id=showid, user=request.user).address}))
	else:#防止伪造get，删除不属于自己的朋友
		c = Context({"title":"查看地图", "message":"失败！此联系人不在您的朋友列表中！", "url":"/", "urltext":"点此返回" })
		return render_to_response("message.html", c)

@login_required
def addrecord(request):
    """
    第一次进入，POST为空，直接渲染add.html。
    提交后，第二次进入此函数，POST非空，新建记录，重定向到根目录。
    """
    if request.POST:
        post = request.POST
        new_friend = Friend(
            user = request.user,
            name = post["name"],
            qq = post["qq"],
            renren = post["renren"],
            address = post["address"])       
        new_friend.save()
        return HttpResponseRedirect("/")
    return render_to_response("add.html")

def showrecord(request):
	"""
	若用户已登录，则显示其通讯录。否则，显示欢迎页面，提示用户登录或注册。
	"""
	if request.user.is_authenticated():
		username = request.user.username
		friend_list = Friend.objects.filter(user = request.user)
		c = Context({"friend_list": friend_list, "username": username, "count": len(friend_list), })
		return render_to_response("index.html", c)
	else:
		return render_to_response("welcome.html")
	
@login_required
def deleterecord(request):
	dltid = request.GET["id"]
	if len(Friend.objects.filter(id=dltid, user=request.user)) > 0:
		Friend.objects.filter(id=dltid).delete()
		return HttpResponseRedirect("/")
	else:#防止伪造get，删除不属于自己的朋友
		c = Context({"title":"删除朋友", "message":"删除失败！此联系人不在您的朋友列表中！", "url":"/", "urltext":"点此返回" })
		return render_to_response("message.html", c)
	
@login_required
def updaterecord(request):
	"""
	第一次进入，POST为空，GET有一个id，渲染update.html。
	点击保存后，第二次进入此函数，POST非空，直接更新数据并跳转到根目录。
	"""
	if request.POST:
		post = request.POST
		p = Friend.objects.get(id=post["id"])
		p.name = post["name"]
		p.renren = post["renren"]
		p.qq = post["qq"]
		p.address = post["address"]
		p.save()
		return HttpResponseRedirect("/")
	elif request.GET:
		if len(Friend.objects.filter(id=request.GET["id"], user = request.user))>0:
			friend = Friend.objects.get(id=request.GET["id"])
			c = Context({"p": friend,})
			return render_to_response("update.html", c)
		else:
			#防止用户伪造get，修改不属于自己的数据
			c = Context({"title":"更新朋友", "message":"更新失败！该联系人不在您的朋友列表中。", "url":"/", "urltext":"点此返回" })
			return render_to_response("message.html", c)
	else:
		return HttpResponseRedirect("/")

@login_required
def search(request):
	word=""
	if request.POST:
		word = request.POST["word"]
		if request.POST["mode"]=="1":#模糊搜索，包含关键字即可
			p = Friend.objects.filter(name__icontains=word, user = request.user)
		else:#精确搜索，需要关键字完全匹配
			p = Friend.objects.filter(name=word, user = request.user)
		c = Context({"result_list": p, "result_len": len(p)})
		return render_to_response("result.html", c)
	return HttpResponseRedirect("/")

@login_required
def chpwd(request):
	"""
	需要检测输入的原密码是否正确、两个新密码是否相同。
	"""
	c = Context({})
	if request.POST:
		notsame=False
		oldwrong=False
		success=False
		old = request.POST["old"]
		new1 = request.POST["new1"]
		new2 = request.POST["new2"]
		if request.user.check_password(old):
			if new1==new2:
				request.user.set_password(new1)
				request.user.save()
				success=True
			else:
				notsame = True
		else:
			oldwrong = True
		c = Context({'notsame': notsame, 'oldwrong': oldwrong, 'success': success, })
	return render_to_response("registration/changepassword.html", c)
	
def reg(request):
	"""
	当用户没有登录时，显示注册页面。
	对用户的注册信息进行检查。
	"""
	if request.user.is_authenticated():
		c = Context({"title":"错误", "message":"您已登陆！如果想要注册新用户，请先登出！", "url":"/accounts/logout/", "urltext":"点此登出" })
		return render_to_response("message.html", c)
	else:
		if request.POST:
			name = request.POST["username"]
			mail = request.POST["email"]
			pass1 = request.POST["password1"]
			pass2 = request.POST["password2"]
			
			empty = False
			namevalid = True
			passvalid = True
			success = False
			if name=="" or mail=="" or pass1=="" or pass2=="":
				empty = True
			u = User.objects.filter(username=name)
			if len(u)>0:
				namevalid = False
			if pass1 != pass2:
				passvalid = False
			if (not empty) and namevalid and passvalid:
				user = User.objects.create_user(username = name, email = mail, password = pass1)
				user.is_staff = True #使用户拥有网站的管理权限
				user.save()
				success = True
			return render_to_response("registration/register.html",{'invalidname': not namevalid, 'invalidpass': not passvalid, 'success': success, 'empty': empty, })
		else:
			return render_to_response("registration/register.html")