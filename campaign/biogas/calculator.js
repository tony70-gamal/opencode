function fmt(n){return n.toLocaleString("en-EG",{maximumFractionDigits:0})}
function fmt1(n){return n.toLocaleString("en-EG",{maximumFractionDigits:1})}
function calc(){
  const waste = parseFloat(document.getElementById("waste").value)||0;
  const days = parseFloat(document.getElementById("days").value)||0;
  const disp = parseFloat(document.getElementById("dispCost").value)||0;
  const kwhPrice = parseFloat(document.getElementById("kwhPrice").value)||0;
  const y = parseFloat(document.getElementById("yield").value)||0;
  const ch4 = (parseFloat(document.getElementById("ch4").value)||60)/100;
  const eff = (parseFloat(document.getElementById("eff").value)||30)/100;
  const annualWaste = waste*days;
  const biogas = annualWaste*y;
  const theoKwh = biogas*ch4*9.97;
  const elec = theoKwh*eff;
  const dispSave = annualWaste*disp;
  const enSave = elec*kwhPrice;
  const benefit = dispSave+enSave;
  document.getElementById("oWaste").textContent = fmt(annualWaste)+" kg/yr";
  document.getElementById("oBiogas").textContent = fmt(biogas)+" m3/yr";
  document.getElementById("oEnergy").textContent = fmt(theoKwh)+" kWh/yr";
  document.getElementById("oElec").textContent = fmt(elec)+" kWh/yr";
  document.getElementById("oDisp").textContent = fmt(dispSave)+" EGP/yr";
  document.getElementById("oEnSave").textContent = fmt(enSave)+" EGP/yr";
  document.getElementById("oBenefit").textContent = fmt(benefit)+" EGP/yr";
}
["waste","days","ch4","eff"].forEach(id=>{
  const el=document.getElementById(id);
  if(!el) return;
  el.addEventListener("input",()=>{
    const v=el.value;
    if(id==="waste") document.getElementById("wasteVal").textContent=v+" kg";
    if(id==="days") document.getElementById("daysVal").textContent=v;
    if(id==="ch4") document.getElementById("ch4Val").textContent=v+"%";
    if(id==="eff") document.getElementById("effVal").textContent=v+"%";
    calc();
  });
});
["dispCost","kwhPrice","yield"].forEach(id=>{
  const el=document.getElementById(id);
  if(el) el.addEventListener("input",calc);
});
window.addEventListener("load",calc);
