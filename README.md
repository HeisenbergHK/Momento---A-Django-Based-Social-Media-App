# Momento - A Django-Based Social Media App

Momento is a fully functional social media application built using Django. It allows users to sign up, post images, follow other users, and interact with their posts. Whether you're sharing moments or exploring others' posts, Momento brings people together through visual storytelling.

## Features

**User Authentication:** Secure signup, login, and logout functionality.

**Profile Management:** Update your bio, location, and profile picture.

**Post Creation:** Upload images with captions and share them with your followers.

**Social Interaction:** Follow/unfollow other users and like/unlike their posts.

**Feed:** View posts from users you follow and discover new users to follow.

**Search:** Find users by their username.

## Technologies Used

**Backend:** Django (Python)

**Frontend:** HTML, CSS, Bootstrap

**Database:** SQLite (default), PostgreSQL (optional for production)

**Image Processing:** Pillow

**AJAX:** For seamless like/unlike functionality

**Version Control:** Git

## Getting Started

Follow these steps to set up and run Momento on your local machine.

### Prerequisites
- Python 3.8 or higher

- pip (Python package manager)

### Installation

1. Clone the Repository:
```
git clone https://github.com/your-username/momento.git
cd momento
```

2. Create a Virtual Environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies:
```
pip install -r requirements.txt
```

4. Run Migrations:
```
python manage.py migrate
```

5. Create a Superuser (Optional):
```
python manage.py createsuperuser
```

6. Run the Development Server:
```
python manage.py runserver
```

7. Access the App:
Open your browser and navigate to http://127.0.0.1:8000/.

## Project Structure
```
momento/
├── core/                  # Main app directory
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   ├── __init__.py
│   ├── admin.py           # Admin panel configuration
│   ├── apps.py
│   ├── models.py          # Database models
│   ├── tests.py
│   ├── urls.py            # App-specific URLs
│   └── views.py           # Business logic
├── media/                 # User-uploaded images
├── static/                # Static files (CSS, JS, images)
├── templates/             # Base templates
├── Momento/               # Project settings and configurations
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # Project-wide URLs
│   └── wsgi.py
├── db.sqlite3             # SQLite database (development)
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## Contributing

Contributions are welcome! If you'd like to contribute to Momento, please follow these steps:

1. Fork the repository.

2. Create a new branch ```(git checkout -b feature/YourFeatureName)```

3. Commit your changes ```(git commit -m 'Add some feature')```

4. Push to the branch ```(git push origin feature/YourFeatureName)```

5. Open a pull request.

## Future Improvements

- **Comments and Replies:** Allow users to comment on posts and reply to comments.

- **Direct Messaging: **Implement a private messaging system.

- **Notifications:** Add real-time notifications for new followers, likes, and comments.

- **Advanced Search:** Introduce filters for searching users by location or interests.

- **Post Analytics:** Provide insights into post performance (e.g., views, likes).

- **Multi-Image Posts:** Allow users to upload multiple images in a single post.

## License
This project is licensed under the MIT License.

## Contact

**Hassan Kalantari**

**Email:** hasan.kalantari29@gmail.com

**GitHub:** https://github.com/HeisenbergHK

**LinkedIn:** https://linkedin.com/in/hassan-kalantari-a86ba5173