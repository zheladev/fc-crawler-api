from fc_api.models import User, Post, Thread


def serialize_user(user: User) -> dict:
    return {
        'fc_id': user.fc_id,
        'name': user.name,
        'status': user.status,
        'created_at': user.created_at,
    }


def serialize_post(post: Post) -> dict:
    return {
        'fc_id': post.fc_id,
        'thread_fc_id': post.thread_fc_id,
        'user_fc_id': post.user_fc_id,
        'posted_at': post.posted_at,
        'content': post.content,
    }


def serialize_thread(thread: Thread) -> dict:
    return {
        'fc_id': thread.fc_id,
        'user_fc_id': thread.user_fc_id,
        'posted_at': thread.posted_at,
        'title': thread.title,
    }
