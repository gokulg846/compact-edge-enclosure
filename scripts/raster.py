"""Small orthographic software z-buffer for honest CAD mesh renders without GUI/OpenGL."""
import numpy as np
from matplotlib.colors import to_rgb

def rasterize(triangles,colors,width=1500,height=1050):
 t=np.asarray(triangles,float)
 view=np.array([1.,-1.35,.95]);view/=np.linalg.norm(view)
 right=np.cross([0.,0.,1.],view);right/=np.linalg.norm(right)
 up=np.cross(view,right)
 pts=np.stack([t@right,t@up,t@view],axis=-1)
 lo=pts[:,:,:2].min(axis=(0,1));hi=pts[:,:,:2].max(axis=(0,1));span=hi-lo
 scale=min((width-60)/span[0],(height-60)/span[1]);mid=(lo+hi)/2
 pts[:,:,0]=(pts[:,:,0]-mid[0])*scale+width/2
 pts[:,:,1]=height/2-(pts[:,:,1]-mid[1])*scale
 bg=np.array(to_rgb('#f5f7fa'))*255
 rgb=np.broadcast_to(bg,(height,width,3)).copy().astype(np.uint8);depth=np.full((height,width),-np.inf)
 light=np.array([-.2,-.5,1.]);light/=np.linalg.norm(light)
 normals=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);norm=np.linalg.norm(normals,axis=1)
 for i,tri in enumerate(pts):
  if norm[i]<1e-12:continue
  n=normals[i]/norm[i]
  if n@view<=0:continue
  x0,y0,z0=tri[0];x1,y1,z1=tri[1];x2,y2,z2=tri[2]
  den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
  if abs(den)<1e-12:continue
  xmin=max(0,int(np.floor(min(x0,x1,x2))));xmax=min(width-1,int(np.ceil(max(x0,x1,x2))))
  ymin=max(0,int(np.floor(min(y0,y1,y2))));ymax=min(height-1,int(np.ceil(max(y0,y1,y2))))
  if xmin>xmax or ymin>ymax:continue
  yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
  a=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/den
  b=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/den;c=1-a-b
  zz=a*z0+b*z1+c*z2
  db=depth[ymin:ymax+1,xmin:xmax+1]
  mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)&(zz>db)
  db[mask]=zz[mask]
  shade=.60+.40*max(0,n@light)
  rgb[ymin:ymax+1,xmin:xmax+1][mask]=np.clip(np.array(to_rgb(colors[i]))*255*shade,0,255).astype(np.uint8)
 return rgb
