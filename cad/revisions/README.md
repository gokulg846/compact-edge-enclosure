# Digital design history

Rev A: first CAD baseline used a rounded rectangular pocket (94 × 64, R3, start3,3), four cylindrical lid bosses radius4 at 6/94,6/64, and PCB pitch 72 × 42. Rev B replaces the pocket with the rounded stepped outline in model.py and moves PCB pitch to 64 × 34. The JSON snapshots record both parameter states; there was no physical test between them.

To reconstruct early Rev A, use rev-a.json and replace the cavity block in build(): `pocket=rounded(L-2*w,W-2*w,b,p['pocket_radius'],w,w,p['floor'])`. Before drilling each lid hole, union `cyl(p['lid_boss_radius'],b,x,y)`. This historical geometry is not a manufacturing release and is not covered by final validation. Rev B output is the reviewed package.

Rev C retains the nominal geometry and replaces the unused lid_boss_radius input with corner_island_width. The shared cavity function is the current geometry source. Rev C snapshots also guard the reviewed PDF tables and analysis assumptions. Do not use Rev A/B schema files directly with the current builder.
