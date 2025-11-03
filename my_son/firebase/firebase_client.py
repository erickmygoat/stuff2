import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseClient:
    """
    A client to handle interactions with Firebase services, including Firestore.
    """
    def __init__(self, service_account_key_path):
        """
        Initializes the Firebase Admin SDK and the Firestore client.

        Args:
            service_account_key_path (str): The file path to the Firebase service account key.
        """
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_key_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_config(self, user_id):
        """
        Retrieves the configuration document for a specific user.

        In line with the instructions, this function fetches the 'first_mover_config'
        document associated with the given userId.

        Args:
            user_id (str): The ID of the user whose configuration is to be retrieved.

        Returns:
            dict: The configuration data as a dictionary, or None if not found.
        """
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('configs').document('first_mover_config')
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                print(f"No configuration found for user {user_id}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching configuration: {e}")
            return None

    def update_data(self, collection, document, data):
        """
        Updates a document in a specified collection.

        Args:
            collection (str): The name of the collection.
            document (str): The name of the document.
            data (dict): The data to update in the document.
        """
        try:
            doc_ref = self.db.collection(collection).document(document)
            doc_ref.update(data)
            print(f"Document {document} in collection {collection} updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating data: {e}")

    def get_data(self, collection, document):
        """
        Retrieves a document from a specified collection.

        Args:
            collection (str): The name of the collection.
            document (str): The name of the document.

        Returns:
            dict: The document data, or None if not found.
        """
        try:
            doc_ref = self.db.collection(collection).document(document)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                print(f"No such document: {document} in collection {collection}")
                return None
        except Exception as e:
            print(f"An error occurred while retrieving data: {e}")
            return None
