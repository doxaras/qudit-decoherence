"""The r=6 'fair' Shor instance under all three gate-cost models."""
import json, os, time
from concurrent.futures import ProcessPoolExecutor
from qudit_shor import shor_run, shor_config, multiplicative_order, recovered_order

N, A = 21, 2   # r = 6: representable in NO base
def floor(d):
    m,_ = shor_config(d,N); D=d**m; r=multiplicative_order(A,N)
    return sum(recovered_order(y,D,A,N)==r for y in range(D))/D
def one(args):
    d,nm,cm,s = args
    t0=time.time(); r=shor_run(d,nm,s,a=A,N=N,cost_model=cm)
    return dict(d=d,noise=nm,cost=cm,strength=s,success=float(r["success"]),
                layers=r["n_layers"],elapsed=round(time.time()-t0,1))
if __name__=="__main__":
    fl={d:floor(d) for d in (2,3,5)}
    bl={d:shor_run(d,a=A,N=N)["success"] for d in (2,3,5)}
    for d in (2,3,5): print(f"d={d}: floor={fl[d]:.3f} noiseless={bl[d]:.3f}",flush=True)
    jobs=[(d,nm,cm,0.005) for nm in ("transmon_cal","depolarizing")
          for cm in ("uniform","ion","pavlidis") for d in (2,3,5)]
    out=[]
    with ProcessPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one,jobs):
            r["signal"]=(r["success"]-fl[r["d"]])/(bl[r["d"]]-fl[r["d"]])
            out.append(r)
            print(f"{r['noise']:13s} {r['cost']:9s} d={r['d']} "
                  f"layers={r['layers']:6.1f} signal={r['signal']:6.3f}",flush=True)
    json.dump({"N":N,"a":A,"floor":fl,"baseline":bl,"runs":out},
              open("results/fair_shor.json","w"),indent=1)
    print("\nwrote results/fair_shor.json")
