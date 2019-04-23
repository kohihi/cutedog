var app = new Vue({
	el: '#app',
	data: {
		message: 'Hello Vue!',
		show: {},
		imgList: [],
		comments: {}
	},
	mounted() {
		this.getImg()
	},
	methods: {
		getImg: function(page) {
			var path = `/api/image`
			var data = {
				"page": page
			}
			var that = this
			ajax("GET", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					that.imgList = r.data
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
			var author = e("#author").value
			var data = {
				"url": url,
				"author": author
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
		},

		voteOk: function(event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 1,
			}
			var path = `/api/vote`
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					alert("投票成功")
				} else {
					alert(r.code)
				}

			})
		},

		voteNo: function(event) {
			var data = {
				"img_id": parseInt(event.target.parentElement.parentElement.dataset.imgid),
				"type": 0,
			}
			var path = `/api/vote`
			ajax("PUT", path, data, function(r) {
				r = JSON.parse(r)
				if (r.code == 0) {
					alert("投票成功")
				} else {
					alert(r.code)
				}

			})
		}
	}
})

