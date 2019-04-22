var app = new Vue({
	el: '#app',
	data: {
		message: 'Hello Vue!'
	},
	methods: {
		submitUrl: function() {
			var url = e("#url-text").value
			var author = e("#author").value
			var data = {
				"url": url,
				"author": author
			}
			path = `/api/image`
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
				"img_id": parseInt(event.target.parentElement.dataset.imgid),
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
				"img_id": parseInt(event.target.parentElement.dataset.imgid),
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