var app = new Vue({
	el: '#app',
	data: {
		message: 'Hello Vue!'
	},
	methods: {
		submitUrl: function () {
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
		}
	}
})