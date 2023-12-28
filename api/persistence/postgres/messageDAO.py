from __future__ import absolute_import
from persistence.DAO import MessageDAO
from model.Message import Message
from .__init__ import *

class PostgresMessageDAO(MessageDAO):

    def getMessages(self, args: dict) -> list:
        # Initial query to be modified
        query = ''' SELECT messages.id, message, edited, timestamp, username, chatname
                    FROM messages
                    INNER JOIN chats ON messages.chat_id = chats.id
                    INNER JOIN users ON messages.user_id = users.id
                    WHERE chatname = %s'''
        
        # The only required argument is the chatname to filter by
        chatname = args.get('chatname')

        # Arguments that will be passed alongside the query
        query_args = [chatname] 
            
        for key in args.keys():
            match (key):
                case 'contains':
                    query += '\nAND LOWER(message) LIKE \'%%\' || %s || \'%%\''
                case 'before':
                    query += '\nAND timestamp < %s'
                case 'after':
                    query += '\nAND timestamp > %s'
                case 'username':
                    query += '\nAND username = %s'
                case _:
                    continue
            query_args.append(args.get(key))

        query += """
            ORDER BY timestamp DESC;
        """
        return exec_get_all(query, query_args)
    
    def createMessage(self, message: Message) -> int:
        pass

    def deleteMessage(self, id: int) -> None:
        pass

    def editMessage(self, message: Message) -> None:
        pass
