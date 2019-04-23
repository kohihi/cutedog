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
		author: 'Anonymous'
	},
	mounted() {
		this.getImg(1)
		this.author = getCookie('author')
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
					alert(code)
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
					alert(code)
				}
			})
		},

		submitUrl: function() {
			var url = e("#url-text").value
			const regex = /^\s*$/
			if (regex.test(url)) {
				return
			}
			var data = {
				"url": url,
				"author": this.author
			}
			var path = `/api/image`
			ajax("POST", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
                    alert("is ok")
                } else {
                    alert("not ok")
                }
			})
			e("#url-text").value = ""
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
                    alert("ok")
                    that.comments[img_id].push(r.data)
                    e("#CTA-"+img_id).value = ""
                } else {
                    alert("not ok:" + r.code)
                }
			})
		},

		voteOk: function(index, event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 1,
			}
			var path = `/api/vote`
			var that = this
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList[index].ok += 1
					alert("投票成功")
				} else {
					alert(r.code)
				}

			})
		},

		voteNo: function(index, event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 0,
			}
			var path = `/api/vote`
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList[index].no += 1
					alert("投票成功")
				} else {
					alert(r.code)
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
	}
})

