# pylint: disable=arguments-differ

"""Content Class for mongo backend."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId

from forum.models.contents import Contents


class CommentThread(Contents):
    """
    CommentThread class for cs_comments_service content model
    """

    content_type = "CommentThread"

    def get_votes(
        self, up: Optional[List[str]] = None, down: Optional[List[str]] = None
    ) -> Dict[str, object]:
        """
        Calculates and returns the vote summary for a thread.

        Args:
            up (list, optional): A list of user IDs who upvoted the thread.
            down (list, optional): A list of user IDs who downvoted the thread.

        Returns:
            dict: A dictionary containing the vote summary with the following keys:
                - "up" (list): The list of user IDs who upvoted.
                - "down" (list): The list of user IDs who downvoted.
                - "up_count" (int): The count of upvotes.
                - "down_count" (int): The count of downvotes.
                - "count" (int): The total number of votes (upvotes + downvotes).
                - "point" (int): The vote score (upvotes - downvotes).
        """
        up = up or []
        down = down or []
        votes = {
            "up": up,
            "down": down,
            "up_count": len(up),
            "down_count": len(down),
            "count": len(up) + len(down),
            "point": len(up) - len(down),
        }
        return votes

    def insert(  # type: ignore
        self,
        title: str,
        body: str,
        course_id: str,
        commentable_id: str,
        author_id: str,
        author_username: str,
        anonymous: bool = False,
        anonymous_to_peers: bool = False,
        thread_type: str = "discussion",
        context: str = "course",
    ) -> str:
        """
        Inserts a new thread document into the database.

        Args:
            title (str): The title of the thread.
            body (str): The body content of the thread.
            course_id (str): The ID of the course the thread is associated with.
            commentable_id (str): The ID of the commentable entity.
            author_id (str): The ID of the author who created the thread.
            author_username (str): The username of the author.
            anonymous (bool, optional): Whether the thread is posted anonymously. Defaults to False.
            anonymous_to_peers (bool, optional): Whether the thread is anonymous to peers. Defaults to False.
            thread_type (str, optional): The type of the thread, either 'question' or 'discussion'.
            context (str, optional): The context of the thread, either 'course' or 'standalone'.

        Raises:
            ValueError: If `thread_type` is not 'question' or 'discussion'.
            ValueError: If `context` is not 'course' or 'standalone'.

        Returns:
            str: The ID of the inserted document.
        """
        if thread_type not in ["question", "discussion"]:
            raise ValueError("Invalid thread_type")

        if context not in ["course", "standalone"]:
            raise ValueError("Invalid context")

        date = datetime.now()
        thread_data = {
            "votes": self.get_votes(up=[], down=[]),
            "abuse_flaggers": [],
            "historical_abuse_flaggers": [],
            "thread_type": thread_type,
            "context": context,
            "comment_count": 0,
            "at_position_list": [],
            "title": title,
            "body": body,
            "course_id": course_id,
            "commentable_id": commentable_id,
            "_type": self.content_type,
            "anonymous": anonymous,
            "anonymous_to_peers": anonymous_to_peers,
            "closed": False,
            "author_id": author_id,
            "author_username": author_username,
            "created_at": date,
            "updated_at": date,
            "last_activity_at": date,
        }
        result = self._collection.insert_one(thread_data)
        return str(result.inserted_id)

    def update(  # type: ignore
        self,
        thread_id: str,
        thread_type: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        course_id: Optional[str] = None,
        anonymous: Optional[bool] = None,
        anonymous_to_peers: Optional[bool] = None,
        commentable_id: Optional[str] = None,
        at_position_list: Optional[List[str]] = None,
        closed: Optional[bool] = None,
        context: Optional[str] = None,
        author_id: Optional[str] = None,
        author_username: Optional[str] = None,
        votes: Optional[Dict[str, int]] = None,
        abuse_flaggers: Optional[List[str]] = None,
        closed_by: Optional[str] = None,
        pinned: Optional[bool] = None,
        comments_count: Optional[int] = None,
        endorsed: Optional[bool] = None,
    ) -> int:
        """
        Updates a thread document in the database.

        Args:
            thread_id: ID of thread to update.
            thread_type: The type of the thread, either 'question' or 'discussion'.
            title: The title of the thread.
            body: The body content of the thread.
            course_id: The ID of the course the thread is associated with.
            anonymous: Whether the thread is posted anonymously.
            anonymous_to_peers: Whether the thread is anonymous to peers.
            commentable_id: The ID of the commentable entity.
            at_position_list: A list of positions for @mentions.
            closed: Whether the thread is closed.
            context: The context of the thread, either 'course' or 'standalone'.
            author_id: The ID of the author who created the thread.
            author_username: The username of the author.
            votes: The votes for the thread.
            abuse_flaggers: A list of users who flagged the thread for abuse.
            closed_by: The ID of the user who closed the thread.
            pinned: Whether the thread is pinned.
            comments_count: The number of comments on the thread.
            endorsed: Whether the thread is endorsed.

        Returns:
            int: The number of documents modified.
        """
        fields = [
            ("thread_type", thread_type),
            ("title", title),
            ("body", body),
            ("course_id", course_id),
            ("anonymous", anonymous),
            ("anonymous_to_peers", anonymous_to_peers),
            ("commentable_id", commentable_id),
            ("at_position_list", at_position_list),
            ("closed", closed),
            ("context", context),
            ("author_id", author_id),
            ("author_username", author_username),
            ("votes", votes),
            ("abuse_flaggers", abuse_flaggers),
            ("closed_by", closed_by),
            ("pinned", pinned),
            ("comments_count", comments_count),
            ("endorsed", endorsed),
        ]
        update_data: dict[str, Any] = {
            field: value for field, value in fields if value is not None
        }

        date = datetime.now()
        update_data["updated_at"] = date
        update_data["last_activity_at"] = date
        result = self._collection.update_one(
            {"_id": ObjectId(thread_id)},
            {"$set": update_data},
        )
        return result.modified_count
