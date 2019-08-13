def includeme(config):
    ca = config.add_route
    ca('api.health', '/health')

    ###
    # USERS
    ###
    ca('users', '/users')
    ca('users.detail', '/users/{fc_id}')

    ###
    # THREADS
    ###
    ca('threads', '/threads')
    ca('threads.detail', '/threads/{fc_id}')

    ###
    # POSTS
    ###
    ca('posts', '/posts')
    ca('posts.detail', '/posts/{fc_id}')
