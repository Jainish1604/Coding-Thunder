if "user" in session and session['user']==params['admin_user']:
    #     posts = Posts.querry.all()
    #     return render_template("Dashboard.html", params=params, posts=posts)

    # if request.method=="POST":
    #     username = request.form.get("uname")
    #     userpass = request.form.get("upass")
    #     if username==params['admin_user'] and userpass==params['admin_password']:
    #         # set the session variable
    #         session['user']=username
    #         posts = Posts.querry.all()
    #         return render_template("Dashboard.html", params=params, posts=posts)
    # else: 