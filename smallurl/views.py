from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from smallurl.models import HashedURL, Redirect
from django.template import loader
from django.db.models import F
import random
#    return HttpResponse('OK') # 200
#    return HttpResponseRedirect('/uri/') # 302
#    return HttpResponsePermanentRedirect('/uri/') # 301
#
# 301 is perm, passes credit to long URL, search engine goes to redirect
# 302 is temp, credit stops here, users wont like this if they want credit
# 200 is all good, only use that for shorten page

# Create your views here.
alphabet = [chr(i) for i in range(ord('a'),ord('z')+1)] +[chr(i) for i in range(ord('A'),ord('Z')+1)] + [chr(i) for i in range(ord('0'),ord('9')+1)]
base = len(alphabet)

CURRENT_SITE_DOMAIN = '138.68.255.118/'

def redir(request):
	if request.method == 'POST':
		return redir_post(request)
	else:
		return redir_get(request)

def redir_post(request):
	url_orig = request.POST.get("url")
	url = url_orig
	#check if empty url
	if url == None or len(url) == 0:
		return shorten(request)	#EMPTY URL
	#check if there is a scheme there
	scheme_index = url.find('://')
	#default scheme is http
	if scheme_index < 0:
		url = 'http://' + url
	elif scheme_index == 0:
		url = 'http' + url #somehow url start with, ://*
	#if there is a custom hash
	h = request.POST.get("hash")
	h = hash_and_save_url(url, h, request)
	if h:
		template = 'submitted.html'
		context = {
			'url': url_orig,
			'small_url': CURRENT_SITE_DOMAIN + h
		}
		return render(request, template, context)
	else:
		return shorten(request, hash_path=h)	#TAKEN

def redir_get(request):
	hash_path = request.get_full_path()
	if len(hash_path) <= 1:
		return shorten(request)	#EMPTY THEY SHOULD BE HERE
	hash_path = hash_path[1:]
	try:
		obj = HashedURL.objects.get(hash=hash_path)
	except HashedURL.DoesNotExist:
		obj = None
	if obj:
		update_stats(request, obj)
		return HttpResponsePermanentRedirect(obj.url)
	else:
		return shorten(request, hash_path=hash_path)	#INVALID HASH

def update_stats(request, hashedUrl):
	#hashedUrl Must not be None Here, we already just checked
	ip = get_client_ip(request)
	referer = get_referer(request)
	user_agent = request.META.get('HTTP_USER_AGENT')
	redirect_stat = Redirect(hashedUrl = hashedUrl, referer = referer, ip = ip, user_agent = user_agent)
	redirect_stat.save()

def shorten(request, hash_path = None):
	template = 'shorten.html'
	context = {'hash': hash_path}
	return render(request, template, context)

def hash_and_save_url(url, h, request):
	if len(h) > 0:
		if HashedURL.objects.filter(hash=h).exists():
			return None
	else:
		attempts = 0
		h = createHash(str(random.random()) + url)
		while HashedURL.objects.filter(hash=h).exists():
			if attempts > 10:
				return None
			attempts += 1
			h = createHash(str(random.random()) + url)
	ip = get_client_ip(request)
	hashedUrl = HashedURL(hash=h,url=url, ip=ip)
	hashedUrl.save()
	return h

def createHash(longUrl):
	hashVal = hash(longUrl)
	if hashVal == 0:
		hashVal = random.randint(1,9223372036854775807)
	outHash = ''
	counter = 0
	if hashVal < 0:
		hashVal *= -1
	while hashVal > 0 and counter < 7:
		r = hashVal % base
		outHash += alphabet[r]
		counter = counter + 1
		hashVal /= base
	return outHash

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def get_referer(request):
	referer = request.META.get('HTTP_REFERER')
	if referer:
		return referer
	return ''