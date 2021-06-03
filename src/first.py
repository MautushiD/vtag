from lib import *
app = QApplication(sys.argv)

path_project = "/Users/jchen/Dropbox/projects/Virtual_Tags/data/One_Pig"
os.chdir(path_project)

name_imgs = os.listdir()
name_imgs.sort()


# Load files
window = 60
imgs_rgb = np.zeros((window, 480, 848, 3), dtype=np.uint8)
for i in range(window):
    imgs_rgb[i] = cv.imread(name_imgs[i])

imgs_bw = imgs_rgb.sum(axis=3)

img = detect_imgs(img=imgs_bw, frame=40)
plt.imshow(img)


# Test QPixmap
i = 20
qp = QPixmap(name_imgs[i])
qb = np2qt(detect_imgs(img=imgs_bw, frame=i))




plt.imshow(qp.toImage())


f0 = [34, 35, 36, 37]
w  = [2]*4
out = []

for i in range(4):
    out += [get_binary(imgs_bw, f0[i], f0[i] + w[i], cut=0.5)]

# Plotting
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
ax[0, 0].imshow(out[0])
ax[0, 0].set_title("%d-%d frames" % (f0[0], f0[0] + w[0] - 1))
ax[0, 1].imshow(out[1])
ax[0, 1].set_title("%d-%d frames" % (f0[1], f0[1] + w[1] - 1))
ax[1, 0].imshow(out[2])
ax[1, 0].set_title("%d-%d frames" % (f0[2], f0[2] + w[2] - 1))
ax[1, 1].imshow(out[3])
ax[1, 1].set_title("%d-%d frames" % (f0[3], f0[3] + w[3] - 1))



i = 40
img = detect_imgs(img=imgs_bw, frame=i)

# i = 40
rgy = [20, 250]
rgx = [240, 450]
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 4))
# i = 20
# rgy = [20, 300]
# rgx = [360, 600]
ax[0].imshow(img[rgy[0]:rgy[1], rgx[0]:rgx[1]])
ax[0].set_title("Detection")
ax[1].imshow(imgs_bw[i][rgy[0]:rgy[1], rgx[0]:rgx[1]])
ax[1].set_title("Raw")



fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 4))
ax[0].imshow(img)
ax[0].set_title("Detection")
ax[1].imshow(imgs_bw[i])
ax[1].set_title("Raw")







plt.imshow(turn_img_to_clusters(out[0], 2))
plt.imshow(turn_img_to_clusters(out[1], 2))
plt.imshow(turn_img_to_clusters(out[2], 2))


import imutils
img_c = turn_img_to_clusters(out[0], 2).astype(np.uint8)
img_c = cv.GaussianBlur(img_c, (5, 5), 0)


cnts = cv.findContours((img_c==0).astype(np.uint8), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)
cts = max(cnts, key=cv.contourArea).reshape(-1, 2)

plt.figure()
plt.imshow(img_c)
plt.plot(cts[:, 0], cts[:, 1], "red")
plt.show()
#####



# draw the contours of c


cv.drawContours(img_c, [c], -1, (0, 0, 255), 2)


# show the output image
cv.imshow("Image", img_c)
cv.waitKey(0)



gm = GaussianMixture(n_components=2, random_state=0).fit(imgb)
gm.predict(imgb).shape
plt.imshow(thresh)



contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cts = contours[14].reshape(-1, 2)
plt.figure()
plt.imshow(img)
plt.plot(cts[:, 0], cts[:, 1], "red")
plt.show()




ret, thresh = cv.threshold(out[0], 127, 255, 0)
plt.imshow(thresh)
thresh.max()

contours, hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]
rect = cv.minAreaRect(cnt)
box = cv.boxPoints(rect)
box = np.int0(box)
img_test = cv.drawContours(out[0], [box], 0, (0, 0, 255), 2)
plt.imshow(img_test)
plt.imshow(box)



out_bin = get_binary(out[0])
plt.imshow(out_bin)

plt.imshow(out[0] + out[1])


x = out[1] - out[0]
x[x<0] = 0
plt.imshow(imgs[35])
plt.imshow(x)
plt.imshow(out[1])

plt.imshow(imgs2[35])

out[0]


34 5 6 7
5 6 7 8
6 7 8 9
7 8 9 10
