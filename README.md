# 📽️ Video API Documentation

## Overview

This RESTful API allows users to **create**, **retrieve**, **update**, and **delete** video entries using Flask, Flask-RESTful, and SQLAlchemy. It uses an SQLite database to persist data.

---

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-RESTful**: Simplifies building REST APIs
- **Flask-SQLAlchemy**: ORM for database interaction
- **SQLite**: Database

---

## 📦 Database Model

### `VideoModel`

| Field | Type | Description |
|-------|------|-------------|
| `id` | `Integer` | Primary Key |
| `name` | `String(100)` | Name of the video, required |
| `views` | `Integer` | Number of views, required |
| `likes` | `Integer` | Number of likes, required |

---

## 📥 Request Parsers

### PUT (`/video/<int:video_id>`)

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `name`   | `str` | ✅ Yes | Name of the video |
| `views`  | `int` | ✅ Yes | Number of views |
| `likes`  | `int` | ✅ Yes | Number of likes |

### PATCH (`/video/<int:video_id>`)

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `name`   | `str` | ❌ No | Updated name |
| `views`  | `int` | ❌ No | Updated views |
| `likes`  | `int` | ❌ No | Updated likes |

---

## 📤 Resource Fields (Response Format)

```json
{
  "id": 1,
  "name": "Sample Video",
  "views": 100,
  "likes": 10
}
```

---

## 🚀 Endpoints

### `GET /video/<int:video_id>`

- **Description**: Fetches a video by its ID.
- **Response**:
  - `200 OK` with video data
  - `404 Not Found` if video ID doesn't exist

---

### `PUT /video/<int:video_id>`

- **Description**: Creates a new video with the provided ID.
- **Body**: JSON with `name`, `views`, and `likes`.
- **Response**:
  - `201 Created` with video data
  - `409 Conflict` if video ID already exists

---

### `PATCH /video/<int:video_id>`

- **Description**: Updates an existing video with the provided fields.
- **Body**: Partial or full JSON with `name`, `views`, `likes`.
- **Response**:
  - `200 OK` with updated video
  - `404 Not Found` if video doesn't exist

---

### `DELETE /video/<int:video_id>`

- **Description**: Deletes the video with the given ID.
- **Note**: This endpoint currently contains an error (see issues below).
- **Response**:
  - `204 No Content` if successful
  - `404 Not Found` if video doesn't exist

---

## ⚠️ Known Issues / To Fix

1. **DELETE Method Bug**:
   - Uses `del videos[video_id]`, but `videos` is undefined. Should instead remove the video from the database:
     ```python
     result = VideoModel.query.filter_by(id=video_id).first()
     if not result:
         abort(404, message="Video doesn't exist, cannot delete")
     db.session.delete(result)
     db.session.commit()
     return '', 204
     ```

2. **String Representation Bug in `__repr__`**:
   - Should reference instance variables:
     ```python
     def __repr__(self):
         return f"Video(name={self.name}, views={self.views}, likes={self.likes})"
     ```

---

## ▶️ Running the App

```bash
python app.py
```

Make sure to initialize the database first:

```python
from your_script_name import db
db.create_all()
```


