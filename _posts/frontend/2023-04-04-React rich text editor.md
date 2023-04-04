---
layout: post
title: "React rich text editor"
date: 2023-04-04
categories: Frontend
tags:
  - React
  - js
---

there are many rich text editors, such as [draft.js](https://draftjs.org/), [quill.js](https://quilljs.com/), [slate.js](https://www.slatejs.org/), etc.

quill is a good choice for me, because it is easy to use and opensource.

in the React, we can use [react-quill](https://github.com/zenoamaro/react-quill), the example code is:

```js
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

const editorModules = {
  toolbar: [
    [{ header: [1, 2, false] }],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [
      { list: "ordered" },
      { list: "bullet" },
      { indent: "-1" },
      { indent: "+1" },
    ],
    ["link", "image", "video"],
    ["clean"],
  ],
};

<ReactQuill theme="snow" modules={editorModules} />;
```

image and video is pasted link in above example.  
if we want upload image, we can use [https://github.com/noeloconnell/quill-image-uploader](https://github.com/noeloconnell/quill-image-uploader):

```js
import ReactQuill, {Quill } from "react-quill";
...
import ImageUploader from "quill-image-uploader";

const editorModules = {
  toolbar: [
    ...
  ],
  imageUploader: {
    upload: (file) => {
      return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append("image", file);
        fetch(`${your api}`, {
          method: "POST",
          body: formData,
        })
          .then((response) => response.json())
          .then((result) => {
            console.log(result);
            resolve(`${result.url}`);
          })
          .catch((error) => {
            reject("Upload failed");
            console.error("Error:", error);
          });
      });
    },
  },
};
```

backend api in python flask:

```python
@bp.route('/', methods=('POST', ))
def upload_view():
    """上传图片
    """
    file = request.files['file']
    name, ext = os.path.splitext(file.filename)
    filename = name + datetime.now().strftime("%Y%m%d%H%M%S%f") + ext
    file.save(os.path.join(FILE_DIRECTORY, filename))
    return jsonify({"url": f"{bp.url_prefix}{filename}"})
```

what about video, we can use [ngx-quill-upload](https://openbase.com/js/ngx-quill-upload/documentation), this library can handle both image and video.

```js
...
import { ImageHandler, VideoHandler } from "ngx-quill-upload";

Quill.register("modules/videoHandler", VideoHandler);
Quill.register("modules/imageHandler", ImageHandler);

const uploadFile = (file) => {
  return new Promise((resolve, reject) => {
    const formData = new FormData();
    formData.append("file", file);
    fetch(`${your api}`, {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        resolve(`${result.url}`);
      })
      .catch((error) => {
        reject("Upload failed");
        console.error("Error:", error);
      });
  });
};

const editorModules = {
  toolbar: [
    ...
  ],
  imageHandler: {
    upload: uploadFile,
  },
  videoHandler: {
    upload: uploadFile,
  },
}

...
```

backend code is same as above.
