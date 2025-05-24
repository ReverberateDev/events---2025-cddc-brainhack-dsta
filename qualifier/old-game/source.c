void entry(void)

{
  int *piVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  long in_FS_OFFSET;
  undefined4 unaff_retaddr;
  undefined auStack_10030 [65520];
  undefined8 uStack_40;
  undefined *puStack_38;
  undefined4 auStack_30 [2];
  undefined *puStack_28;
  undefined4 uStack_18;
  undefined *puStack_10;
  
  puStack_10 = &stack0x00000008;
  DAT_005cee68 = auStack_30;
  DAT_005cee60 = auStack_10030;
  piVar1 = (int *)cpuid_basic_info(0);
  iVar3 = piVar1[2];
  iVar4 = piVar1[3];
  if (*piVar1 != 0) {
    if (((piVar1[1] == 0x756e6547) && (iVar3 == 0x49656e69)) && (iVar4 == 0x6c65746e)) {
      DAT_0062e51c = 1;
    }
    puVar2 = (undefined4 *)cpuid_Version_info(1);
    _DAT_0062e574 = *puVar2;
    iVar3 = puVar2[2];
    iVar4 = puVar2[3];
  }
  DAT_005cee70 = DAT_005cee60;
  DAT_005cee78 = DAT_005cee60;
  uStack_18 = unaff_retaddr;
  if (DAT_005ce040 == (code *)0x0) {
    puStack_38 = (undefined *)0x4656b7;
    FUN_00469580(&DAT_005cf6e8,puStack_10,iVar3,iVar4);
    *(undefined8 *)(in_FS_OFFSET + -8) = 0x123;
    if (DAT_005cf6e8 != 0x123) {
      puStack_38 = (undefined *)0x4656d8;
      FUN_00467560();
    }
  }
  else {
    puStack_38 = (undefined *)0x465691;
    DAT_005cee68 = auStack_30;
    (*DAT_005ce040)(&DAT_005cee60,&DAT_00464a60,0,0);
    DAT_005cee70 = DAT_005cee60 + 0x3a0;
    DAT_005cee78 = DAT_005cee70;
  }
  *(undefined ***)(in_FS_OFFSET + -8) = &DAT_005cee60;
  DAT_005cf660 = &DAT_005cee60;
  DAT_005cee90 = &DAT_005cf660;
  puStack_38 = (undefined *)0x4656fc;
  FUN_00469d80();
  auStack_30[0] = uStack_18;
  puStack_28 = puStack_10;
  puStack_38 = (undefined *)0x465712;
  FUN_00469d40();
  puStack_38 = (undefined *)0x465717;
  FUN_00469b60();
  puStack_38 = (undefined *)0x46571c;
  FUN_00469ca0();
  puStack_38 = &DAT_0051cfa8;
  uStack_40 = 0x465729;
  FUN_00469d00();
  puStack_38 = (undefined *)0x46572f;
  FUN_004657a0();
  puStack_38 = (undefined *)0x465734;
  FUN_00467560();
  return;
}