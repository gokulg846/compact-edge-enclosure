"""Lumped steady-state thermal model; assumptions, NOT measured performance."""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]

def temperature(q,ambient,r_contact,r_spreading,r_air):
    values=[q,ambient,r_contact,r_spreading,r_air]
    if not all(math.isfinite(v) for v in values):raise ValueError('finite inputs required')
    if q<0 or min(r_contact,r_spreading,r_air)<0:raise ValueError('heat and resistance must be nonnegative')
    return ambient+q*(r_contact+r_spreading+r_air)

def calculate():
    # R_contact includes compressed TIM + two contact interfaces; not an intrinsic material property.
    Q,T=8.,35.
    configs={'passive':6.0,'forced':2.0}
    out={'status':'CALCULATED FROM ASSUMED RESISTANCES; NOT TESTED','heat_W':Q,'ambient_C':T,'limit_case_C':80,'R_contact_K_W':.8,'R_spreading_K_W':.5,'configurations':{}}
    for name,r in configs.items():
        total=.8+.5+r
        out['configurations'][name]={'R_air_K_W':r,'R_total_K_W':total,'case_C':temperature(Q,T,.8,.5,r),'max_heat_at_80C_W':(80-T)/total,'target_met_nominal':temperature(Q,T,.8,.5,r)<=80}
    # Corner sweep includes TIM/contact and effective air-side uncertainty.
    out['uncertainty_at_8W_35C']={n:{'low_C':temperature(8,35,.4,.3,lo),'high_C':temperature(8,35,1.6,.8,hi)} for n,(lo,hi) in {'passive':(4,10),'forced':(1,4)}.items()}
    # Gap = base seat height + lid pedestal offset - PCB support stack - chip.
    out['pad_stack_mm']={'nominal_gap':.5,'worst_case_sum':.03+.03+.03+.05+.05,'gap_min':.31,'gap_max':.69,'pad_free_min':.95,'pad_free_max':1.05,'compression_min_pct':(1-.69/.95)*100,'compression_max_pct':(1-.31/1.05)*100,'RSS_reference_only':math.sqrt(3*.03**2+2*.05**2)}
    return out

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    data=calculate();(ROOT/'results/thermal.json').write_text(json.dumps(data,indent=2)+'\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(10,5.4),layout='constrained');fig.set_facecolor('#f7f9fc');ax.set_facecolor('#f7f9fc')
    q=np.linspace(0,12,100)
    for name,c,bounds in [('passive','#d78328',(4.7,12.4)),('forced','#077f83',(1.7,6.4))]:
        r=data['configurations'][name]['R_total_K_W'];ax.plot(q,35+q*r,color=c,lw=2.5,label=f'{name.capitalize()} assumption: {r:.1f} K/W total')
        ax.fill_between(q,35+q*bounds[0],35+q*bounds[1],color=c,alpha=.10)
        ax.scatter([8],[35+8*r],color=c,zorder=4)
    ax.axhline(80,color='#a43838',ls='--',label='80 C case screening target')
    ax.axvline(8,color='#6e7d91',ls=':',lw=1)
    ax.set(xlabel='Applied heat load [W]',ylabel='Estimated component case temperature [C]',title='Thermal sensitivity | 35 C ambient',xlim=(0,12),ylim=(30,160))
    ax.grid(alpha=.15);ax.legend(loc='upper left',fontsize=9)
    fig.text(.99,.01,'Bands: assumption corners, not statistical confidence intervals',ha='right',fontsize=8,color='#53647c')
    for ext in ['png','svg']:fig.savefig(ROOT/'images'/f'thermal_sensitivity.{ext}',dpi=180)
    plt.close(fig);print(json.dumps(data,indent=2))
if __name__=='__main__':main()
