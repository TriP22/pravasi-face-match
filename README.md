
# Finding your look alike celebrity

![Python](https://img.shields.io/badge/Python-3.9-yellow)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)
![Dataset](https://img.shields.io/badge/Dataset-Kaggle-blue)

We all are very curious about comparing ourselfs to other. Imagine comparing your facial features with Bollywood celebrities
to find your lookalike celeb.

Using MTCNN and VggFACE, created a webApp where you could upload your image and the model tells you to which Bollywood celeb your 
face lookalike to.

![homepage](https://user-images.githubusercontent.com/94764266/153998956-771d1f09-3d86-4628-ae90-4cbc9961f50a.JPG)

## Local Deployment

#### Clone the repository

```bash
git clone https://github.com/EphronM/Celebrity_face_match.git
```

#### Download the dataset from kaggle

- [Bollywood Celebrity Faces](https://www.kaggle.com/havingfun/100-bollywood-celebrity-faces) (images of 100 Bollywood celebrities)

![image](https://user-images.githubusercontent.com/94764266/153993051-3e83f02b-1aa6-4468-9ed7-694d3fe93a12.png)

* Combine all the folders into a single folder named `data` 

#### Create a conda environment after opening the repository

```bash
conda create -n face_env python=3.9 -y
```

```bash
conda activate face_env
```


- Installing the required dependencies
```bash
pip install -r requirements.txt
```

#### Creating artifacts

* Croping celeb face and saving it in `data cropped`

```bash
  python src\01_genreating_image_pickle.py
```
* Extracting features from all the images and saving the pickle file

```bash
  python src\02_feature_extraction.py
```

**We are using MTCNN as the face detector and VggFace prediction model to extract the feature similarities. Finally using Cosine Similarity, we find the similar celeb face.**



#### All set to deploy

```bash
  streamlit run app.py
```



## Model performence

Lets give the model few real bollywood celeb look alikes peoples photos and see,

![result1](https://user-images.githubusercontent.com/94764266/153999261-ec87b1d0-7f0a-41ff-b7b0-3c76fc755c53.JPG)

Works well with `David Saharia` who is real life tiger shroff lookalike


Lets try it with the `Amitabh Bachchan` transformed look.


![Captaure](https://user-images.githubusercontent.com/94764266/153999364-09e17ed7-b400-4d51-97ca-e10202b3481a.JPG)

worked good with 75% match.

![result2](https://user-images.githubusercontent.com/94764266/153998675-b98282cc-a148-43d9-9973-754646f7b0bd.JPG) ![Capture](https://user-images.githubusercontent.com/94764266/153998682-0a5dceaf-eab2-462a-83bb-b407bffbe763.JPG)



This all about this project. 

Happy coding Focks!!


```bash
Author: EphronM
Email: ephronmartin2016@gmail.com

```

