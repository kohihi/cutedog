var ajax = function(method, path, data, responseCallback) {
  if (method == "GET") {
    if (data != "") {
      var args = '?'
      for (p in data) {
        args += p + "=" + data[p] + "&"
      }
      path += args
    }
  }
  var r = new XMLHttpRequest()
  r.open(method, path, true)
  r.setRequestHeader('Content-Type', 'application/json')
  r.onreadystatechange = function() {
    if(r.readyState === 4) {
      responseCallback(r.response)
    }
  }
  data = JSON.stringify(data)
  r.send(data)
}

var e = function(sel) {
  return document.querySelector(sel)
}

var eAll = function(sel) {
  return document.querySelectorAll(sel)
}

var setCookie = function(c_name, value, expiredays) {
  var exdate=new Date()
  exdate.setDate(exdate.getDate()+expiredays)
  document.cookie=c_name+ "=" + escape(value)
                  +((expiredays==null) ? "" : ";expires="+exdate.toGMTString()
                  +";path=/")
}

var getCookie = function(c_name) {
  if (document.cookie.length>0) {
    c_start = document.cookie.indexOf(c_name + "=")
    if (c_start != -1) {
      c_start = c_start + c_name.length+1
      c_end = document.cookie.indexOf(";",c_start)
      if (c_end == -1) c_end=document.cookie.length
      return unescape(document.cookie.substring(c_start,c_end))
      }
    }
  return ""
}


var clear_board = function() {
    $("#id_chat_area").val('');
}

const socket = io.connect('ws://' + document.domain + ':' + location.port + '/chat');
socket.on('connect', function() {
    console.log('connect');
    clear_board();
});

socket.on('status', function(data) {
    $('#id_chat_area').val($('#id_chat_area').val() + '<' + data.msg + '>\n');
    $('#id_chat_area').scrollTop($('#id_chat_area')[0].scrollHeight);
});
socket.on('message', function(data) {
	console.log("message")
    $('#id_chat_area').val($('#id_chat_area').val() + data.msg + '\n');
    $('#id_chat_area').scrollTop($('#id_chat_area')[0].scrollHeight);
});
socket.on('update_online', function(data) {
	console.log("update")
	$('#id_current_online').text(data.msg)
});
socket.on('error_handler', function(data) {
	console.log('has error')
	if(data.code == 10000) {
		return
	}
	alert(data.msg)
});


var app = new Vue({
	el: '#app',
	data: {
		message: 'Hello Vue!',
		show: {},
		imgList: [],
		comments: {},
		current_page: 0,
		max_page: 0,
		current_board: 'all',
		author: 'Anonymous',
		chatName: 'Anonymous',
		hasChatName: false,
		chatChannel: 'wangmiao',
		message:"",
		alert: false,
		joined: false,
		joinBtnText: "LINK START"
	},
	mounted() {
		this.getImg(1)
		var author = getCookie('author')
		if (author != "") {
			this.author = author
		}
		var chatName = getCookie('chatName')
		if (chatName != "") {
			this.chatName = chatName
		}
	},
	filters: {
		dateFormat: function(value) {
			var a = new Date() - new Date(value)
			a = parseInt(a/1000)
			if (a > 2592000) {
				return value.split(" ")[0]
			} 
			if (a > 86400) {
				return (parseInt(a / 86400)+"天前")
			}
			if (a > 3600) {
				return(parseInt(a / 3600)+"小时前")
			}
			if (a > 60) {
				return(parseInt(a / 60)+"分钟前")
			}
			if (a > 0) {
				return(a+"秒前")
			} else {
				return("刚刚")
			}
		}
	},
	methods: {
		getImg: function(page, board='all') {
			var path = `/api/image`
			var data = {
				"page": page,
				"board": board
			}
			var that = this
			ajax("GET", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList = r.data
					that.current_page = page
					that.current_board = board
					that.max_page = r.next
				} else {
					alert("error:code" + r.code)
				}
			})
		},

		getComments: function(event) {
			var path = `/api/image/comment`
			var params = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
			}
			this.show[params.img_id] = !this.show[params.img_id]
			var that = this
			ajax("GET", path, params, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					Vue.set(that.comments, params.img_id, r.data)
				} else {
					alert("error:code" + r.code)
				}
			})
		},

		submitUrl: function() {
			var inputUrl = e("#text-url")
			var inputWord = e('#text-word')
			var url = inputUrl.value
			var word=((inputWord.value.replace(/<(.+?)>/gi,"&lt;$1&gt;")).replace(/ /gi,"&nbsp;")).replace(/\n/gi,"<br>")
			var board = e("#select-board").value
			const regex = /^\s*$/
			if (regex.test(url)) {
				return
			}
			var data = {
				"author": this.author,
				"url": url,
				"word": word,
				"board": board
			}
			var path = `/api/image`
			var that = this
			ajax("POST", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
                    that.alertText("已提交")
                    inputUrl.value = ""
                    inputWord.value = ""
                } else {
                    alert("error:code" + r.code)
                }
			})
		},

		submitComment: function(img_id) {
			var content = e("#CTA-"+img_id).value
			const regex = /^\s*$/
			if (regex.test(content)) {
				return
			}
			var data = {
				"img_id": img_id,
				"author": this.author,
				"content": content
			}
			var path = `/api/image/comment`
			var that = this
			ajax("POST", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
                    that.comments[img_id].push(r.data)
                    e("#CTA-"+img_id).value = ""
                } else {
                    alert("error:code" + r.code)
                }
			})
		},

		voteW: function(index, event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 1,
			}
			var path = `/api/vote`
			var that = this
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList[index].w += 1
					that.alertText("汪!")
				} else {
					that.alertText("已经点过汪了")
				}

			})
		},

		voteM: function(index, event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 0,
			}
			var path = `/api/vote`
			var that = this
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList[index].m += 1
					that.alertText("喵~")
				} else {
					that.alertText("已经点过喵了")
				}

			})
		},

		setPage: function(page) {
			window.scroll(0, 0)
			if (page == "next") {
				this.getImg(this.current_page+1, this.board)
			} else if (page == "prev") {
				this.getImg(this.current_page-1, this.board)
			} else {
				this.getImg(page, this.board)
			}
		},

		setAuthor: function() {
			var a = e("#author").value
			const regex = /^\s*$/
			if (regex.test(a)) {
				alert("名字不能全是空白符")
				return
			}
			setCookie("author", a, 365)
			this.author = a
			e("#author").value = ""
		},

		alertText: function(text) {
			this.message = text
			this.alert = true
			var t = setTimeout(() => {
				this.alert = false
			}, 2000, t)
		},

		joinRoLeftRoom: function() {
			if(this.joined) {
				socket.emit('left', {room:this.chatChannel, name:encodeURI(this.chatName)})
				this.joined = false
				this.joinBtnText = "进入房间"
				var msg = "<你已离开房间>"
				$('#id_chat_area').val($('#id_chat_area').val() + msg + '\n');
    			$('#id_chat_area').scrollTop($('#id_chat_area')[0].scrollHeight);
			} else {
				socket.emit('joined', {room:this.chatChannel, name:encodeURI(this.chatName)})
				this.joined = true
				this.joinBtnText = "离开房间"
			}
		},

		sendMsg: function() {
			if(this.joined == false) {
				this.alertText("未进入房间")
				return
			}
			var text = e('#id_chat_text').value
			text = encodeURI(text)
			e('#id_chat_text').value = ""
			socket.emit('text', {msg:text, room:this.chatChannel, name:encodeURI(this.chatName)})
		},

		disconnect: function() {
			socket.disconnect()
			this.joined = false
			this.joinBtnText = "LINK START"
			clear_board()
		},

		setChatName: function() {
			var a = e("#id_chat_name").value
			const regex = /^\s*$/
			if (regex.test(a)) {
				this.alertText("名字不能全是空白符")
				return
			}
			this.chatName = a
		},
	}
})
