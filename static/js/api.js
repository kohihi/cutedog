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


// api方法示例
var apiBriefingInfo = function(bid, callBack) {
    var args = {
        "briefing_id": bid,
    }
    var path = `/api/briefing`
    ajax("GET", path, args, callBack)
}
