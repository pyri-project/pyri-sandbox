from pyri.sandbox import blockly_compiler
import io

def _do_blockly_compile_test(blockly_json, expected_pysrc):
    json_io = io.StringIO(blockly_json)
    output_io = io.StringIO()

    blockly_compiler.compile_blockly_file(json_io, output_io)
    output_io.seek(0)
    pysrc_str = output_io.read()
    print(pysrc_str)
    assert pysrc_str == expected_pysrc

def test_blockly_compiler_simple():
    hello_world_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "ig-@O/ylKy_@*tL~m@X|",
        "x": 138,
        "y": 88,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "hello_world_blockly"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "text_print",
              "id": "leNnyydaklEu0$|E4fU~",
              "inputs": {
                "TEXT": {
                  "shadow": {
                    "type": "text",
                    "id": "wWggJq|t$BAzKbOf`dtu",
                    "fields": {
                      "TEXT": "Hello World from Blockly!"
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }
}
"""
    expected_pysrc = "# Describe this function...\ndef hello_world_blockly():\n  print('Hello World from Blockly!')\n"

    _do_blockly_compile_test(hello_world_blockly_json, expected_pysrc)
    

def test_blockly_compiler_util():
    util_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "util_blocks_test"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "controls_if",
              "id": "F{=dnOZN]sG+fG-3h;^%",
              "inputs": {
                "IF0": {
                  "block": {
                    "type": "logic_compare",
                    "id": "Dh@tqs[sHdA_MqxfdtiF",
                    "fields": {
                      "OP": "EQ"
                    },
                    "inputs": {
                      "A": {
                        "block": {
                          "type": "proc_result_get",
                          "id": "?AYk5LTN?T@}}2hkLJt*"
                        }
                      },
                      "B": {
                        "block": {
                          "type": "text",
                          "id": "#7W`UujXgZ+bo.P4w}9F",
                          "fields": {
                            "TEXT": "SUCCESS"
                          }
                        }
                      }
                    }
                  }
                },
                "DO0": {
                  "block": {
                    "type": "variables_set",
                    "id": "IeMDhdVG03z::vVoPW!i",
                    "fields": {
                      "VAR": {
                        "id": "8W]t2tv|VPY:Y~k2qqbR"
                      }
                    },
                    "inputs": {
                      "VALUE": {
                        "block": {
                          "type": "proc_result_get",
                          "id": ":z64:%~JM|zW9r*_k^$a"
                        }
                      }
                    }
                  }
                }
              },
              "next": {
                "block": {
                  "type": "variables_set",
                  "id": "ImQBTRFQQd7ps`:#pxKO",
                  "fields": {
                    "VAR": {
                      "id": "8W]t2tv|VPY:Y~k2qqbR"
                    }
                  },
                  "inputs": {
                    "VALUE": {
                      "block": {
                        "type": "util_copy",
                        "id": "*hYW(m?AmR7LczD#B2Ai",
                        "inputs": {
                          "VALUE": {
                            "block": {
                              "type": "text",
                              "id": "L-@aEntN#Ul_#~:o;sEl",
                              "fields": {
                                "TEXT": "aaaa"
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  },
  "variables": [
    {
      "name": "val",
      "id": "8W]t2tv|VPY:Y~k2qqbR"
    }
  ]
}
"""

    expected_pysrc = "# Describe this function...\ndef util_blocks_test():\n\n  if (proc_result_get()) == 'SUCCESS':\n    val = proc_result_get()\n  val = util_copy('aaaa')\n"
    
    _do_blockly_compile_test(util_blockly_json, expected_pysrc)

def test_blockly_compiler_globals():
    globals_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "globals_test"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "controls_if",
              "id": "DDo-TIrJG/+lK|:Yvl$B",
              "inputs": {
                "IF0": {
                  "block": {
                    "type": "logic_compare",
                    "id": "}!6CP-{xEOzNfZ2y2^6{",
                    "fields": {
                      "OP": "LTE"
                    },
                    "inputs": {
                      "A": {
                        "block": {
                          "type": "math_number",
                          "id": "nDS0r-NWZ.)G*%^7n;H*",
                          "fields": {
                            "NUM": 2
                          }
                        }
                      },
                      "B": {
                        "block": {
                          "type": "global_variable_get",
                          "id": "xPaL9ulJsFu3=[/am=M6",
                          "fields": {
                            "NAME": "bad_var"
                          }
                        }
                      }
                    }
                  }
                },
                "DO0": {
                  "block": {
                    "type": "controls_repeat_ext",
                    "id": "]doJ0%t[v]yWt3tl;7^/",
                    "inputs": {
                      "TIMES": {
                        "block": {
                          "type": "math_number",
                          "id": "{2GZNW2+~ggs}llpJ*ix",
                          "fields": {
                            "NUM": 3
                          }
                        }
                      },
                      "DO": {
                        "block": {
                          "type": "global_variable_set",
                          "id": "+9E2hvnFj}5ZGGoyDG0k",
                          "fields": {
                            "NAME": "my_global"
                          },
                          "inputs": {
                            "VALUE": {
                              "block": {
                                "type": "text",
                                "id": "N{`,[vS.w-T8xg$]_L%@",
                                "fields": {
                                  "TEXT": "bbbbb"
                                }
                              }
                            }
                          },
                          "next": {
                            "block": {
                              "type": "variables_set",
                              "id": "N(S?:vUl%1vbJQ:LX~/}",
                              "fields": {
                                "VAR": {
                                  "id": "2vzd@Kudw-oD(Y+,2^j,"
                                }
                              },
                              "inputs": {
                                "VALUE": {
                                  "block": {
                                    "type": "global_variable_get",
                                    "id": "%CoV`Sh!sNj8W+q|;Vaa",
                                    "fields": {
                                      "NAME": "my_global2"
                                    }
                                  }
                                }
                              },
                              "next": {
                                "block": {
                                  "type": "global_variable_add",
                                  "id": "5hX#dZsRMycf8F!36_Z@",
                                  "fields": {
                                    "TYPE": "NUMBER",
                                    "PERS": "NORMAL"
                                  },
                                  "inputs": {
                                    "NAME": {
                                      "block": {
                                        "type": "text",
                                        "id": "Y7fz,qQ.F9L86EVagTq}",
                                        "fields": {
                                          "TEXT": "abcde"
                                        }
                                      }
                                    },
                                    "VALUE": {
                                      "block": {
                                        "type": "math_number",
                                        "id": "bFESb[yQhG4d})w#a.~/",
                                        "fields": {
                                          "NUM": 1.2345
                                        }
                                      }
                                    },
                                    "RESET_VALUE": {
                                      "block": {
                                        "type": "math_number",
                                        "id": "=ACdmRX1g+XElQj{$L_V",
                                        "fields": {
                                          "NUM": 6.789
                                        }
                                      }
                                    }
                                  },
                                  "next": {
                                    "block": {
                                      "type": "global_variable_delete",
                                      "id": "=?!*iy?DJ][iS|zCq*GX",
                                      "fields": {
                                        "NAME": "my_dumb_var"
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  },
  "variables": [
    {
      "name": "val",
      "id": "2vzd@Kudw-oD(Y+,2^j,"
    }
  ]
}
"""

    expected_pysrc = "# Describe this function...\ndef globals_test():\n\n  if 2 <= (global_variable_get(\"bad_var\")):\n    for count in range(3):\n      global_variable_set(\"my_global\", 'bbbbb')\n      val = global_variable_get(\"my_global2\")\n      global_variable_add('abcde', \"NUMBER\", 1.2345, \"NORMAL\", 6.789)\n      global_variable_delete(\"my_dumb_var\")\n"    
    _do_blockly_compile_test(globals_blockly_json, expected_pysrc)


def test_blockly_compiler_time():
    time_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "test_time"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "time_wait",
              "id": ")MVN2x6X9p8XJ$hmA;_6",
              "fields": {
                "WAIT_TIME": 1
              },
              "next": {
                "block": {
                  "type": "time_wait_for_completion",
                  "id": "~LRXWr17c)IC)*F9tP~!",
                  "fields": {
                    "DEVICE_NAME": "my_robot2",
                    "TIMEOUT": 25.2
                  },
                  "next": {
                    "block": {
                      "type": "time_wait_for_completion_all",
                      "id": "6q4N1-U}bgL-H+QQe^Y%",
                      "fields": {
                        "TIMEOUT": 1.5
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }
}
"""

    expected_pysrc = "# Describe this function...\ndef test_time():\n  time_wait(float(1))\n  time_wait_for_completion(\"my_robot2\", float(25.2))\n  time_wait_for_completion_all(float(1.5))\n"
    _do_blockly_compile_test(time_blockly_json, expected_pysrc)


def test_blockly_compiler_time():
    time_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "test_time"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "time_wait",
              "id": ")MVN2x6X9p8XJ$hmA;_6",
              "fields": {
                "WAIT_TIME": 1
              },
              "next": {
                "block": {
                  "type": "time_wait_for_completion",
                  "id": "~LRXWr17c)IC)*F9tP~!",
                  "fields": {
                    "DEVICE_NAME": "my_robot2",
                    "TIMEOUT": 25.2
                  },
                  "next": {
                    "block": {
                      "type": "time_wait_for_completion_all",
                      "id": "6q4N1-U}bgL-H+QQe^Y%",
                      "fields": {
                        "TIMEOUT": 1.5
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  }
}
"""

    expected_pysrc = "# Describe this function...\ndef test_time():\n  time_wait(float(1))\n  time_wait_for_completion(\"my_robot2\", float(25.2))\n  time_wait_for_completion_all(float(1.5))\n"
    _do_blockly_compile_test(time_blockly_json, expected_pysrc)

def test_blockly_compiler_linalg():
    linalg_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "test_linalg"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "variables_set",
              "id": "F_,S[=cZL)p]iQVdm-Vw",
              "fields": {
                "VAR": {
                  "id": "ln~g.cb)A[bM=g#w%gi9"
                }
              },
              "inputs": {
                "VALUE": {
                  "block": {
                    "type": "linalg_vector",
                    "id": "A})T,CYA}UQUK(0/58Dw",
                    "fields": {
                      "VECTOR": "3.4,5.6,7.8"
                    }
                  }
                }
              },
              "next": {
                "block": {
                  "type": "variables_set",
                  "id": "u@37hL4K4HLLrhdZ.f$s",
                  "fields": {
                    "VAR": {
                      "id": "{NaR7hQ5Wda5(Ws6RPF-"
                    }
                  },
                  "inputs": {
                    "VALUE": {
                      "block": {
                        "type": "linalg_matrix",
                        "id": "/s3*eM:;N*NX*ldbFZ{P",
                        "fields": {
                          "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                        }
                      }
                    }
                  },
                  "next": {
                    "block": {
                      "type": "variables_set",
                      "id": "sFd#gJ{oP8Y(B,}j;m;m",
                      "fields": {
                        "VAR": {
                          "id": ":3mN/aG+cW8efhRAf_OX"
                        }
                      },
                      "inputs": {
                        "VALUE": {
                          "block": {
                            "type": "linalg_fill_vector",
                            "id": "0UT[i,ZN`EJa2aAW.@b!",
                            "inputs": {
                              "M": {
                                "block": {
                                  "type": "math_number",
                                  "id": "_[20?/W35^a@EOik3cyy",
                                  "fields": {
                                    "NUM": 3
                                  }
                                }
                              },
                              "VALUE": {
                                "block": {
                                  "type": "variables_get",
                                  "id": "fc`wvy*NW55INz{Tj82i",
                                  "fields": {
                                    "VAR": {
                                      "id": "[UN{-8NrmBY+@pD(L:S["
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      },
                      "next": {
                        "block": {
                          "type": "variables_set",
                          "id": "m@lCT4i4j#v.*7{Ow!5l",
                          "fields": {
                            "VAR": {
                              "id": ":3mN/aG+cW8efhRAf_OX"
                            }
                          },
                          "inputs": {
                            "VALUE": {
                              "block": {
                                "type": "linalg_fill_matrix",
                                "id": "]EwZvzU)$n)DH|q:v97G",
                                "inputs": {
                                  "M": {
                                    "block": {
                                      "type": "math_number",
                                      "id": "rt|PR~wgX6s#V^w2T07r",
                                      "fields": {
                                        "NUM": 3
                                      }
                                    }
                                  },
                                  "N": {
                                    "block": {
                                      "type": "math_number",
                                      "id": "*}0fo|MKy)(f*;p#tBwi",
                                      "fields": {
                                        "NUM": 4
                                      }
                                    }
                                  },
                                  "VALUE": {
                                    "block": {
                                      "type": "variables_get",
                                      "id": "r}.~zN6DV+Kr#/ggcwu2",
                                      "fields": {
                                        "VAR": {
                                          "id": "[UN{-8NrmBY+@pD(L:S["
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "next": {
                            "block": {
                              "type": "variables_set",
                              "id": "?F3,L~{5$TOVfwvDpx?{",
                              "fields": {
                                "VAR": {
                                  "id": "[UN{-8NrmBY+@pD(L:S["
                                }
                              },
                              "inputs": {
                                "VALUE": {
                                  "block": {
                                    "type": "linalg_unary_op",
                                    "id": "M|R_Zv5cd{D^J9,v9f@u",
                                    "fields": {
                                      "OP": "TRANSPOSE"
                                    },
                                    "inputs": {
                                      "INPUT": {
                                        "block": {
                                          "type": "variables_get",
                                          "id": "2=^Np_8TU1Q^rddZiF;u",
                                          "fields": {
                                            "VAR": {
                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              },
                              "next": {
                                "block": {
                                  "type": "variables_set",
                                  "id": "e60B;9y$gY[.D(3-ET;Q",
                                  "fields": {
                                    "VAR": {
                                      "id": "[UN{-8NrmBY+@pD(L:S["
                                    }
                                  },
                                  "inputs": {
                                    "VALUE": {
                                      "block": {
                                        "type": "linalg_unary_op",
                                        "id": "#fg:^eXO{re04z,=-7/t",
                                        "fields": {
                                          "OP": "INVERSE"
                                        },
                                        "inputs": {
                                          "INPUT": {
                                            "block": {
                                              "type": "variables_get",
                                              "id": "(lrh/D~xB!pOzY.A}^#!",
                                              "fields": {
                                                "VAR": {
                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  },
                                  "next": {
                                    "block": {
                                      "type": "variables_set",
                                      "id": "/KAP6-_|iQbV:a^S+=u!",
                                      "fields": {
                                        "VAR": {
                                          "id": "[UN{-8NrmBY+@pD(L:S["
                                        }
                                      },
                                      "inputs": {
                                        "VALUE": {
                                          "block": {
                                            "type": "linalg_unary_op",
                                            "id": "4/EJ|noWrui6:Y)ExQAE",
                                            "fields": {
                                              "OP": "NEGATIVE"
                                            },
                                            "inputs": {
                                              "INPUT": {
                                                "block": {
                                                  "type": "variables_get",
                                                  "id": "eRT9f8!F#TX;H5%1,0:K",
                                                  "fields": {
                                                    "VAR": {
                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      },
                                      "next": {
                                        "block": {
                                          "type": "variables_set",
                                          "id": "V)!+2/WGh2U[^@{{XQQ/",
                                          "fields": {
                                            "VAR": {
                                              "id": "[UN{-8NrmBY+@pD(L:S["
                                            }
                                          },
                                          "inputs": {
                                            "VALUE": {
                                              "block": {
                                                "type": "linalg_unary_op",
                                                "id": "G_[1nA?;y!z[d=}|h=Fl",
                                                "fields": {
                                                  "OP": "DETERMINANT"
                                                },
                                                "inputs": {
                                                  "INPUT": {
                                                    "block": {
                                                      "type": "variables_get",
                                                      "id": "_Xyza^(hC(vW`++]*RrW",
                                                      "fields": {
                                                        "VAR": {
                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          },
                                          "next": {
                                            "block": {
                                              "type": "variables_set",
                                              "id": "@wQ4iIT)9GHn-wzj5BNY",
                                              "fields": {
                                                "VAR": {
                                                  "id": "[UN{-8NrmBY+@pD(L:S["
                                                }
                                              },
                                              "inputs": {
                                                "VALUE": {
                                                  "block": {
                                                    "type": "linalg_unary_op",
                                                    "id": "gi$=lr8n[t*[:3aLrKJU",
                                                    "fields": {
                                                      "OP": "CONJUGATE"
                                                    },
                                                    "inputs": {
                                                      "INPUT": {
                                                        "block": {
                                                          "type": "variables_get",
                                                          "id": "5Xa%@TG)E=./B|n}aeu-",
                                                          "fields": {
                                                            "VAR": {
                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              },
                                              "next": {
                                                "block": {
                                                  "type": "variables_set",
                                                  "id": "PZYh$5z+M@NCAwLmbU47",
                                                  "fields": {
                                                    "VAR": {
                                                      "id": "[UN{-8NrmBY+@pD(L:S["
                                                    }
                                                  },
                                                  "inputs": {
                                                    "VALUE": {
                                                      "block": {
                                                        "type": "linalg_unary_op",
                                                        "id": "]h9t,Df8iq?v:kc,F]Fl",
                                                        "fields": {
                                                          "OP": "EIGENVALUES"
                                                        },
                                                        "inputs": {
                                                          "INPUT": {
                                                            "block": {
                                                              "type": "variables_get",
                                                              "id": "s[W/IT#wf0;pSlk`[%@:",
                                                              "fields": {
                                                                "VAR": {
                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  },
                                                  "next": {
                                                    "block": {
                                                      "type": "variables_set",
                                                      "id": "w;pINk%SqR)kt?bG.#!;",
                                                      "fields": {
                                                        "VAR": {
                                                          "id": "[UN{-8NrmBY+@pD(L:S["
                                                        }
                                                      },
                                                      "inputs": {
                                                        "VALUE": {
                                                          "block": {
                                                            "type": "linalg_unary_op",
                                                            "id": ")T!3gY;QtiEueG`l-!%W",
                                                            "fields": {
                                                              "OP": "EIGENVECTORS"
                                                            },
                                                            "inputs": {
                                                              "INPUT": {
                                                                "block": {
                                                                  "type": "variables_get",
                                                                  "id": "i(r:-KXrTKuN:dyjrTTB",
                                                                  "fields": {
                                                                    "VAR": {
                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                    }
                                                                  }
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      },
                                                      "next": {
                                                        "block": {
                                                          "type": "variables_set",
                                                          "id": ")9i,M+LNnPm9B,+uhbW;",
                                                          "fields": {
                                                            "VAR": {
                                                              "id": "[UN{-8NrmBY+@pD(L:S["
                                                            }
                                                          },
                                                          "inputs": {
                                                            "VALUE": {
                                                              "block": {
                                                                "type": "linalg_unary_op",
                                                                "id": "%_^~xo.g,`ncO8@J3*38",
                                                                "fields": {
                                                                  "OP": "MIN"
                                                                },
                                                                "inputs": {
                                                                  "INPUT": {
                                                                    "block": {
                                                                      "type": "variables_get",
                                                                      "id": "=EmGIcmp:jWiovS!y)mr",
                                                                      "fields": {
                                                                        "VAR": {
                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                        }
                                                                      }
                                                                    }
                                                                  }
                                                                }
                                                              }
                                                            }
                                                          },
                                                          "next": {
                                                            "block": {
                                                              "type": "variables_set",
                                                              "id": "E=ZT{dlPaSGyExPtCr)F",
                                                              "fields": {
                                                                "VAR": {
                                                                  "id": "[UN{-8NrmBY+@pD(L:S["
                                                                }
                                                              },
                                                              "inputs": {
                                                                "VALUE": {
                                                                  "block": {
                                                                    "type": "linalg_unary_op",
                                                                    "id": "?{uVDmxt2UTZ=tJ[:j5X",
                                                                    "fields": {
                                                                      "OP": "MAX"
                                                                    },
                                                                    "inputs": {
                                                                      "INPUT": {
                                                                        "block": {
                                                                          "type": "variables_get",
                                                                          "id": "FAgZRJJ0,}M4;}H+sHK(",
                                                                          "fields": {
                                                                            "VAR": {
                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                            }
                                                                          }
                                                                        }
                                                                      }
                                                                    }
                                                                  }
                                                                }
                                                              },
                                                              "next": {
                                                                "block": {
                                                                  "type": "variables_set",
                                                                  "id": ")m{ugX)?9j7*Cw0-B-P)",
                                                                  "fields": {
                                                                    "VAR": {
                                                                      "id": "[UN{-8NrmBY+@pD(L:S["
                                                                    }
                                                                  },
                                                                  "inputs": {
                                                                    "VALUE": {
                                                                      "block": {
                                                                        "type": "linalg_unary_op",
                                                                        "id": "@j?/y3T7PPiKl@c~K%V/",
                                                                        "fields": {
                                                                          "OP": "ARGMIN"
                                                                        },
                                                                        "inputs": {
                                                                          "INPUT": {
                                                                            "block": {
                                                                              "type": "variables_get",
                                                                              "id": "]}WV43/rIT:R~Dh1/1u#",
                                                                              "fields": {
                                                                                "VAR": {
                                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                }
                                                                              }
                                                                            }
                                                                          }
                                                                        }
                                                                      }
                                                                    }
                                                                  },
                                                                  "next": {
                                                                    "block": {
                                                                      "type": "variables_set",
                                                                      "id": "qz1v:H,|4{AIiU=cxN4m",
                                                                      "fields": {
                                                                        "VAR": {
                                                                          "id": "[UN{-8NrmBY+@pD(L:S["
                                                                        }
                                                                      },
                                                                      "inputs": {
                                                                        "VALUE": {
                                                                          "block": {
                                                                            "type": "linalg_unary_op",
                                                                            "id": "{gcgO!P7G{XDqG+n~eIf",
                                                                            "fields": {
                                                                              "OP": "ARGMAX"
                                                                            },
                                                                            "inputs": {
                                                                              "INPUT": {
                                                                                "block": {
                                                                                  "type": "variables_get",
                                                                                  "id": "fRV8r+b,n{Ahx!b~~X]Z",
                                                                                  "fields": {
                                                                                    "VAR": {
                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                    }
                                                                                  }
                                                                                }
                                                                              }
                                                                            }
                                                                          }
                                                                        }
                                                                      },
                                                                      "next": {
                                                                        "block": {
                                                                          "type": "variables_set",
                                                                          "id": "49l;44bvAT`%m`fvE~q+",
                                                                          "fields": {
                                                                            "VAR": {
                                                                              "id": "[UN{-8NrmBY+@pD(L:S["
                                                                            }
                                                                          },
                                                                          "inputs": {
                                                                            "VALUE": {
                                                                              "block": {
                                                                                "type": "linalg_unary_op",
                                                                                "id": "8}-s5gY%{9zuzgKF1nna",
                                                                                "fields": {
                                                                                  "OP": "PINV"
                                                                                },
                                                                                "inputs": {
                                                                                  "INPUT": {
                                                                                    "block": {
                                                                                      "type": "variables_get",
                                                                                      "id": "i?^F(m?@7A$drnkf^n)3",
                                                                                      "fields": {
                                                                                        "VAR": {
                                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                        }
                                                                                      }
                                                                                    }
                                                                                  }
                                                                                }
                                                                              }
                                                                            }
                                                                          },
                                                                          "next": {
                                                                            "block": {
                                                                              "type": "variables_set",
                                                                              "id": "I3cR,A-n9w$UwqlH!mF4",
                                                                              "fields": {
                                                                                "VAR": {
                                                                                  "id": "[UN{-8NrmBY+@pD(L:S["
                                                                                }
                                                                              },
                                                                              "inputs": {
                                                                                "VALUE": {
                                                                                  "block": {
                                                                                    "type": "linalg_unary_op",
                                                                                    "id": "8MCFN4oI6gCM_O*Vo^t6",
                                                                                    "fields": {
                                                                                      "OP": "TRACE"
                                                                                    },
                                                                                    "inputs": {
                                                                                      "INPUT": {
                                                                                        "block": {
                                                                                          "type": "variables_get",
                                                                                          "id": "28TR#lD1.H[pzI#v;Wa$",
                                                                                          "fields": {
                                                                                            "VAR": {
                                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                            }
                                                                                          }
                                                                                        }
                                                                                      }
                                                                                    }
                                                                                  }
                                                                                }
                                                                              },
                                                                              "next": {
                                                                                "block": {
                                                                                  "type": "variables_set",
                                                                                  "id": "*bLxuz,#Jlp*PoR^q}_Y",
                                                                                  "fields": {
                                                                                    "VAR": {
                                                                                      "id": "[UN{-8NrmBY+@pD(L:S["
                                                                                    }
                                                                                  },
                                                                                  "inputs": {
                                                                                    "VALUE": {
                                                                                      "block": {
                                                                                        "type": "linalg_unary_op",
                                                                                        "id": "+LvBFlsI2,FmR1]jI8k$",
                                                                                        "fields": {
                                                                                          "OP": "DIAG"
                                                                                        },
                                                                                        "inputs": {
                                                                                          "INPUT": {
                                                                                            "block": {
                                                                                              "type": "variables_get",
                                                                                              "id": "B-YJ^AbFiECfOc+wzf7+",
                                                                                              "fields": {
                                                                                                "VAR": {
                                                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                }
                                                                                              }
                                                                                            }
                                                                                          }
                                                                                        }
                                                                                      }
                                                                                    }
                                                                                  },
                                                                                  "next": {
                                                                                    "block": {
                                                                                      "type": "variables_set",
                                                                                      "id": "RQ}3AzScnf9~#h;S=)Th",
                                                                                      "fields": {
                                                                                        "VAR": {
                                                                                          "id": "[UN{-8NrmBY+@pD(L:S["
                                                                                        }
                                                                                      },
                                                                                      "inputs": {
                                                                                        "VALUE": {
                                                                                          "block": {
                                                                                            "type": "linalg_unary_op",
                                                                                            "id": "RH9.sP_,hE8`]hYykKJq",
                                                                                            "fields": {
                                                                                              "OP": "HAT"
                                                                                            },
                                                                                            "inputs": {
                                                                                              "INPUT": {
                                                                                                "block": {
                                                                                                  "type": "variables_get",
                                                                                                  "id": "0W:s7CMr(_tYwE=$q;0!",
                                                                                                  "fields": {
                                                                                                    "VAR": {
                                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                    }
                                                                                                  }
                                                                                                }
                                                                                              }
                                                                                            }
                                                                                          }
                                                                                        }
                                                                                      },
                                                                                      "next": {
                                                                                        "block": {
                                                                                          "type": "variables_set",
                                                                                          "id": "DBhb%_/)mEj6}Lv,=rVl",
                                                                                          "fields": {
                                                                                            "VAR": {
                                                                                              "id": "[UN{-8NrmBY+@pD(L:S["
                                                                                            }
                                                                                          },
                                                                                          "inputs": {
                                                                                            "VALUE": {
                                                                                              "block": {
                                                                                                "type": "linalg_unary_op",
                                                                                                "id": "t9Vv4m9U(xfUg3Cl_*zA",
                                                                                                "fields": {
                                                                                                  "OP": "SUM"
                                                                                                },
                                                                                                "inputs": {
                                                                                                  "INPUT": {
                                                                                                    "block": {
                                                                                                      "type": "variables_get",
                                                                                                      "id": "/-YRx2hV@Wt3:@%;gZdS",
                                                                                                      "fields": {
                                                                                                        "VAR": {
                                                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                        }
                                                                                                      }
                                                                                                    }
                                                                                                  }
                                                                                                }
                                                                                              }
                                                                                            }
                                                                                          },
                                                                                          "next": {
                                                                                            "block": {
                                                                                              "type": "variables_set",
                                                                                              "id": ")Qth5MoBgMQXTiDJKs+/",
                                                                                              "fields": {
                                                                                                "VAR": {
                                                                                                  "id": "[UN{-8NrmBY+@pD(L:S["
                                                                                                }
                                                                                              },
                                                                                              "inputs": {
                                                                                                "VALUE": {
                                                                                                  "block": {
                                                                                                    "type": "linalg_unary_op",
                                                                                                    "id": "%LS=jN/MtXv[2%Aif5lw",
                                                                                                    "fields": {
                                                                                                      "OP": "MULTIPLY"
                                                                                                    },
                                                                                                    "inputs": {
                                                                                                      "INPUT": {
                                                                                                        "block": {
                                                                                                          "type": "variables_get",
                                                                                                          "id": "x?os`^UoSLpO@z@uV8Ru",
                                                                                                          "fields": {
                                                                                                            "VAR": {
                                                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                            }
                                                                                                          }
                                                                                                        }
                                                                                                      }
                                                                                                    }
                                                                                                  }
                                                                                                }
                                                                                              },
                                                                                              "next": {
                                                                                                "block": {
                                                                                                  "type": "variables_set",
                                                                                                  "id": "[K%.+=he10:!Uev_QLd-",
                                                                                                  "fields": {
                                                                                                    "VAR": {
                                                                                                      "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                    }
                                                                                                  },
                                                                                                  "inputs": {
                                                                                                    "VALUE": {
                                                                                                      "block": {
                                                                                                        "type": "linalg_binary_op",
                                                                                                        "id": "^EWUO8iZ~12!1]`7rkl6",
                                                                                                        "fields": {
                                                                                                          "OP": "MATRIXADD"
                                                                                                        },
                                                                                                        "inputs": {
                                                                                                          "A": {
                                                                                                            "block": {
                                                                                                              "type": "linalg_matrix",
                                                                                                              "id": "?TxM@wT]Z3I{(:KXf*$b",
                                                                                                              "fields": {
                                                                                                                "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                              }
                                                                                                            }
                                                                                                          },
                                                                                                          "B": {
                                                                                                            "block": {
                                                                                                              "type": "variables_get",
                                                                                                              "id": "57J~|Uxi~T2o]Khk+L|Q",
                                                                                                              "fields": {
                                                                                                                "VAR": {
                                                                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                }
                                                                                                              }
                                                                                                            }
                                                                                                          }
                                                                                                        }
                                                                                                      }
                                                                                                    }
                                                                                                  },
                                                                                                  "next": {
                                                                                                    "block": {
                                                                                                      "type": "variables_set",
                                                                                                      "id": "-jxk4UYQ=;1yWh[Og*FX",
                                                                                                      "fields": {
                                                                                                        "VAR": {
                                                                                                          "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                        }
                                                                                                      },
                                                                                                      "inputs": {
                                                                                                        "VALUE": {
                                                                                                          "block": {
                                                                                                            "type": "linalg_binary_op",
                                                                                                            "id": "}LzjXy1;fCf;0wFvdufd",
                                                                                                            "fields": {
                                                                                                              "OP": "MATRIXSUB"
                                                                                                            },
                                                                                                            "inputs": {
                                                                                                              "A": {
                                                                                                                "block": {
                                                                                                                  "type": "linalg_matrix",
                                                                                                                  "id": "}(y#4n;xLDMmJXEAKdop",
                                                                                                                  "fields": {
                                                                                                                    "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                  }
                                                                                                                }
                                                                                                              },
                                                                                                              "B": {
                                                                                                                "block": {
                                                                                                                  "type": "variables_get",
                                                                                                                  "id": "~Lxlq%I1u6:jZUrutzf}",
                                                                                                                  "fields": {
                                                                                                                    "VAR": {
                                                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                    }
                                                                                                                  }
                                                                                                                }
                                                                                                              }
                                                                                                            }
                                                                                                          }
                                                                                                        }
                                                                                                      },
                                                                                                      "next": {
                                                                                                        "block": {
                                                                                                          "type": "variables_set",
                                                                                                          "id": "Q}r0EgLl%FImLonka]ln",
                                                                                                          "fields": {
                                                                                                            "VAR": {
                                                                                                              "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                            }
                                                                                                          },
                                                                                                          "inputs": {
                                                                                                            "VALUE": {
                                                                                                              "block": {
                                                                                                                "type": "linalg_binary_op",
                                                                                                                "id": "jP}wfK9s@m-3)c^cqhp}",
                                                                                                                "fields": {
                                                                                                                  "OP": "MATRIXMULT"
                                                                                                                },
                                                                                                                "inputs": {
                                                                                                                  "A": {
                                                                                                                    "block": {
                                                                                                                      "type": "linalg_matrix",
                                                                                                                      "id": "ybwK/)Kg*8W1?)@vDEK~",
                                                                                                                      "fields": {
                                                                                                                        "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                      }
                                                                                                                    }
                                                                                                                  },
                                                                                                                  "B": {
                                                                                                                    "block": {
                                                                                                                      "type": "variables_get",
                                                                                                                      "id": ".drT-V6oFmv3@]JqNN!{",
                                                                                                                      "fields": {
                                                                                                                        "VAR": {
                                                                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                        }
                                                                                                                      }
                                                                                                                    }
                                                                                                                  }
                                                                                                                }
                                                                                                              }
                                                                                                            }
                                                                                                          },
                                                                                                          "next": {
                                                                                                            "block": {
                                                                                                              "type": "variables_set",
                                                                                                              "id": "SZi8V9Zv|TS7hba|9Ly(",
                                                                                                              "fields": {
                                                                                                                "VAR": {
                                                                                                                  "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                }
                                                                                                              },
                                                                                                              "inputs": {
                                                                                                                "VALUE": {
                                                                                                                  "block": {
                                                                                                                    "type": "linalg_binary_op",
                                                                                                                    "id": "wE!^:!1YJ2/sUg1:_HRN",
                                                                                                                    "fields": {
                                                                                                                      "OP": "ELEMENTADD"
                                                                                                                    },
                                                                                                                    "inputs": {
                                                                                                                      "A": {
                                                                                                                        "block": {
                                                                                                                          "type": "linalg_matrix",
                                                                                                                          "id": "U*OTy|Xko6(VuZb?.k`j",
                                                                                                                          "fields": {
                                                                                                                            "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                          }
                                                                                                                        }
                                                                                                                      },
                                                                                                                      "B": {
                                                                                                                        "block": {
                                                                                                                          "type": "variables_get",
                                                                                                                          "id": "d6fEA:^y(O.iS#w=:LE0",
                                                                                                                          "fields": {
                                                                                                                            "VAR": {
                                                                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                            }
                                                                                                                          }
                                                                                                                        }
                                                                                                                      }
                                                                                                                    }
                                                                                                                  }
                                                                                                                }
                                                                                                              },
                                                                                                              "next": {
                                                                                                                "block": {
                                                                                                                  "type": "variables_set",
                                                                                                                  "id": "s@}AkbE6b?1Zf2*j=]WA",
                                                                                                                  "fields": {
                                                                                                                    "VAR": {
                                                                                                                      "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                    }
                                                                                                                  },
                                                                                                                  "inputs": {
                                                                                                                    "VALUE": {
                                                                                                                      "block": {
                                                                                                                        "type": "linalg_binary_op",
                                                                                                                        "id": "z!UioLp{hYP~r.Sm%e3|",
                                                                                                                        "fields": {
                                                                                                                          "OP": "ELEMENTSUB"
                                                                                                                        },
                                                                                                                        "inputs": {
                                                                                                                          "A": {
                                                                                                                            "block": {
                                                                                                                              "type": "linalg_matrix",
                                                                                                                              "id": "{R2w9D2nX!@_(V#j-S.R",
                                                                                                                              "fields": {
                                                                                                                                "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                              }
                                                                                                                            }
                                                                                                                          },
                                                                                                                          "B": {
                                                                                                                            "block": {
                                                                                                                              "type": "variables_get",
                                                                                                                              "id": "FfU.tc`CB`0*$pv6E6CF",
                                                                                                                              "fields": {
                                                                                                                                "VAR": {
                                                                                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                }
                                                                                                                              }
                                                                                                                            }
                                                                                                                          }
                                                                                                                        }
                                                                                                                      }
                                                                                                                    }
                                                                                                                  },
                                                                                                                  "next": {
                                                                                                                    "block": {
                                                                                                                      "type": "variables_set",
                                                                                                                      "id": "aE0nL4PLb7z$O+)h7=$V",
                                                                                                                      "fields": {
                                                                                                                        "VAR": {
                                                                                                                          "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                        }
                                                                                                                      },
                                                                                                                      "inputs": {
                                                                                                                        "VALUE": {
                                                                                                                          "block": {
                                                                                                                            "type": "linalg_binary_op",
                                                                                                                            "id": "|}dqvQ9EZ8^SVU(S!7k6",
                                                                                                                            "fields": {
                                                                                                                              "OP": "ELEMENTMULT"
                                                                                                                            },
                                                                                                                            "inputs": {
                                                                                                                              "A": {
                                                                                                                                "block": {
                                                                                                                                  "type": "linalg_matrix",
                                                                                                                                  "id": "-0Ew_OYq3;?S?rn|yyMs",
                                                                                                                                  "fields": {
                                                                                                                                    "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              },
                                                                                                                              "B": {
                                                                                                                                "block": {
                                                                                                                                  "type": "variables_get",
                                                                                                                                  "id": "Jn-I*cz$o@N*jnY]+oKh",
                                                                                                                                  "fields": {
                                                                                                                                    "VAR": {
                                                                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                    }
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              }
                                                                                                                            }
                                                                                                                          }
                                                                                                                        }
                                                                                                                      },
                                                                                                                      "next": {
                                                                                                                        "block": {
                                                                                                                          "type": "variables_set",
                                                                                                                          "id": "(hU`PYj}QS1:iDLp[Oy!",
                                                                                                                          "fields": {
                                                                                                                            "VAR": {
                                                                                                                              "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                            }
                                                                                                                          },
                                                                                                                          "inputs": {
                                                                                                                            "VALUE": {
                                                                                                                              "block": {
                                                                                                                                "type": "linalg_binary_op",
                                                                                                                                "id": "6J%[gXD3hl_r}jWWFeJ(",
                                                                                                                                "fields": {
                                                                                                                                  "OP": "ELEMENTDIV"
                                                                                                                                },
                                                                                                                                "inputs": {
                                                                                                                                  "A": {
                                                                                                                                    "block": {
                                                                                                                                      "type": "linalg_matrix",
                                                                                                                                      "id": "s+`!@piszDyc6azQ[}NA",
                                                                                                                                      "fields": {
                                                                                                                                        "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  },
                                                                                                                                  "B": {
                                                                                                                                    "block": {
                                                                                                                                      "type": "variables_get",
                                                                                                                                      "id": "lk=uN8]7l@1tPETtX3y{",
                                                                                                                                      "fields": {
                                                                                                                                        "VAR": {
                                                                                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                        }
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              }
                                                                                                                            }
                                                                                                                          },
                                                                                                                          "next": {
                                                                                                                            "block": {
                                                                                                                              "type": "variables_set",
                                                                                                                              "id": "6PEAGMV1n4BqlZ?Y_bz#",
                                                                                                                              "fields": {
                                                                                                                                "VAR": {
                                                                                                                                  "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                                }
                                                                                                                              },
                                                                                                                              "inputs": {
                                                                                                                                "VALUE": {
                                                                                                                                  "block": {
                                                                                                                                    "type": "linalg_binary_op",
                                                                                                                                    "id": "}3LJC=W~yIyRtl[#WSUQ",
                                                                                                                                    "fields": {
                                                                                                                                      "OP": "DOT"
                                                                                                                                    },
                                                                                                                                    "inputs": {
                                                                                                                                      "A": {
                                                                                                                                        "block": {
                                                                                                                                          "type": "linalg_matrix",
                                                                                                                                          "id": "T:G|7tnczt#~NFU3c9yK",
                                                                                                                                          "fields": {
                                                                                                                                            "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      },
                                                                                                                                      "B": {
                                                                                                                                        "block": {
                                                                                                                                          "type": "variables_get",
                                                                                                                                          "id": "na^]rH5l%mU1#[0gHq=A",
                                                                                                                                          "fields": {
                                                                                                                                            "VAR": {
                                                                                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                            }
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              },
                                                                                                                              "next": {
                                                                                                                                "block": {
                                                                                                                                  "type": "variables_set",
                                                                                                                                  "id": "u(Cc]|Ay(:#D/.nH_z4i",
                                                                                                                                  "fields": {
                                                                                                                                    "VAR": {
                                                                                                                                      "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                                    }
                                                                                                                                  },
                                                                                                                                  "inputs": {
                                                                                                                                    "VALUE": {
                                                                                                                                      "block": {
                                                                                                                                        "type": "linalg_binary_op",
                                                                                                                                        "id": "z$NrCd!+xA4W~vOr4r-*",
                                                                                                                                        "fields": {
                                                                                                                                          "OP": "CROSS"
                                                                                                                                        },
                                                                                                                                        "inputs": {
                                                                                                                                          "A": {
                                                                                                                                            "block": {
                                                                                                                                              "type": "linalg_matrix",
                                                                                                                                              "id": "?g-V}TRz^AUiqMpK*!)F",
                                                                                                                                              "fields": {
                                                                                                                                                "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          },
                                                                                                                                          "B": {
                                                                                                                                            "block": {
                                                                                                                                              "type": "variables_get",
                                                                                                                                              "id": "eLzEHA#4/qNn9gT7cr1c",
                                                                                                                                              "fields": {
                                                                                                                                                "VAR": {
                                                                                                                                                  "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                                }
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  },
                                                                                                                                  "next": {
                                                                                                                                    "block": {
                                                                                                                                      "type": "variables_set",
                                                                                                                                      "id": "}V|BPVzB_w;(g|uXy5gx",
                                                                                                                                      "fields": {
                                                                                                                                        "VAR": {
                                                                                                                                          "id": "UR8}WZnm@Nd5tWyDA,_["
                                                                                                                                        }
                                                                                                                                      },
                                                                                                                                      "inputs": {
                                                                                                                                        "VALUE": {
                                                                                                                                          "block": {
                                                                                                                                            "type": "linalg_binary_op",
                                                                                                                                            "id": "M+?%Jt_QlNsK}epfAhfh",
                                                                                                                                            "fields": {
                                                                                                                                              "OP": "MATRIXSOLVE"
                                                                                                                                            },
                                                                                                                                            "inputs": {
                                                                                                                                              "A": {
                                                                                                                                                "block": {
                                                                                                                                                  "type": "linalg_matrix",
                                                                                                                                                  "id": "3o8c;#3C6(~dAeBIsV$k",
                                                                                                                                                  "fields": {
                                                                                                                                                    "MATRIX": "[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]"
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              },
                                                                                                                                              "B": {
                                                                                                                                                "block": {
                                                                                                                                                  "type": "variables_get",
                                                                                                                                                  "id": "qKDA,I:PyofPS(lpMgMh",
                                                                                                                                                  "fields": {
                                                                                                                                                    "VAR": {
                                                                                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                                    }
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      },
                                                                                                                                      "next": {
                                                                                                                                        "block": {
                                                                                                                                          "type": "variables_set",
                                                                                                                                          "id": "S=OineIcdp@mK]oi55I.",
                                                                                                                                          "fields": {
                                                                                                                                            "VAR": {
                                                                                                                                              "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                            }
                                                                                                                                          },
                                                                                                                                          "inputs": {
                                                                                                                                            "VALUE": {
                                                                                                                                              "block": {
                                                                                                                                                "type": "linalg_vector_get",
                                                                                                                                                "id": "XdSOLg(pt!#0VcgW8G7a",
                                                                                                                                                "inputs": {
                                                                                                                                                  "VECTOR": {
                                                                                                                                                    "block": {
                                                                                                                                                      "type": "variables_get",
                                                                                                                                                      "id": "1FR63d4CFpp^4]0(11HR",
                                                                                                                                                      "fields": {
                                                                                                                                                        "VAR": {
                                                                                                                                                          "id": "ln~g.cb)A[bM=g#w%gi9"
                                                                                                                                                        }
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  },
                                                                                                                                                  "M": {
                                                                                                                                                    "block": {
                                                                                                                                                      "type": "math_number",
                                                                                                                                                      "id": "Wpno`0[V9+X2Q2A~U=sW",
                                                                                                                                                      "fields": {
                                                                                                                                                        "NUM": 2
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          },
                                                                                                                                          "next": {
                                                                                                                                            "block": {
                                                                                                                                              "type": "variables_set",
                                                                                                                                              "id": "3JR9ab|h8-h09fiC]x)`",
                                                                                                                                              "fields": {
                                                                                                                                                "VAR": {
                                                                                                                                                  "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                                }
                                                                                                                                              },
                                                                                                                                              "inputs": {
                                                                                                                                                "VALUE": {
                                                                                                                                                  "block": {
                                                                                                                                                    "type": "linalg_vector_set",
                                                                                                                                                    "id": "vwiNM|)r^Q]B)=bK`fTG",
                                                                                                                                                    "inputs": {
                                                                                                                                                      "VECTOR": {
                                                                                                                                                        "block": {
                                                                                                                                                          "type": "variables_get",
                                                                                                                                                          "id": "wG|*^#FM]Y/n_q8y55^_",
                                                                                                                                                          "fields": {
                                                                                                                                                            "VAR": {
                                                                                                                                                              "id": "ln~g.cb)A[bM=g#w%gi9"
                                                                                                                                                            }
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      },
                                                                                                                                                      "M": {
                                                                                                                                                        "block": {
                                                                                                                                                          "type": "math_number",
                                                                                                                                                          "id": "#8}2(KJpFif@Q^bl[j|A",
                                                                                                                                                          "fields": {
                                                                                                                                                            "NUM": 2
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      },
                                                                                                                                                      "VALUE": {
                                                                                                                                                        "block": {
                                                                                                                                                          "type": "math_number",
                                                                                                                                                          "id": "h#V}=9mN6?h#T5Jh/rb[",
                                                                                                                                                          "fields": {
                                                                                                                                                            "NUM": 3.333
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              },
                                                                                                                                              "next": {
                                                                                                                                                "block": {
                                                                                                                                                  "type": "variables_set",
                                                                                                                                                  "id": "z0%$0tGvG7)Sj[1g@P-O",
                                                                                                                                                  "fields": {
                                                                                                                                                    "VAR": {
                                                                                                                                                      "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                                    }
                                                                                                                                                  },
                                                                                                                                                  "inputs": {
                                                                                                                                                    "VALUE": {
                                                                                                                                                      "block": {
                                                                                                                                                        "type": "linalg_vector_length",
                                                                                                                                                        "id": "MjtaIHujCsx]+V.wj5Wn",
                                                                                                                                                        "inputs": {
                                                                                                                                                          "VECTOR": {
                                                                                                                                                            "block": {
                                                                                                                                                              "type": "variables_get",
                                                                                                                                                              "id": "bRQ+-a0n{M_1jLiDz3}n",
                                                                                                                                                              "fields": {
                                                                                                                                                                "VAR": {
                                                                                                                                                                  "id": "ln~g.cb)A[bM=g#w%gi9"
                                                                                                                                                                }
                                                                                                                                                              }
                                                                                                                                                            }
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  },
                                                                                                                                                  "next": {
                                                                                                                                                    "block": {
                                                                                                                                                      "type": "variables_set",
                                                                                                                                                      "id": "Qj^R?~HE}L:}D?ChMx*T",
                                                                                                                                                      "fields": {
                                                                                                                                                        "VAR": {
                                                                                                                                                          "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                                        }
                                                                                                                                                      },
                                                                                                                                                      "inputs": {
                                                                                                                                                        "VALUE": {
                                                                                                                                                          "block": {
                                                                                                                                                            "type": "linalg_matrix_get",
                                                                                                                                                            "id": "gC^Qeugf544kd|5crv!S",
                                                                                                                                                            "inputs": {
                                                                                                                                                              "MATRIX": {
                                                                                                                                                                "block": {
                                                                                                                                                                  "type": "variables_get",
                                                                                                                                                                  "id": "Xl]8/i`4^7trdn,zp%0R",
                                                                                                                                                                  "fields": {
                                                                                                                                                                    "VAR": {
                                                                                                                                                                      "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                                                    }
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              },
                                                                                                                                                              "M": {
                                                                                                                                                                "block": {
                                                                                                                                                                  "type": "math_number",
                                                                                                                                                                  "id": "jx*-d`,-#Nh#+WmU3O_=",
                                                                                                                                                                  "fields": {
                                                                                                                                                                    "NUM": 2
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              },
                                                                                                                                                              "N": {
                                                                                                                                                                "block": {
                                                                                                                                                                  "type": "math_number",
                                                                                                                                                                  "id": "XqeI-eTO%/OR`.iij[x,",
                                                                                                                                                                  "fields": {
                                                                                                                                                                    "NUM": 3
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              }
                                                                                                                                                            }
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      },
                                                                                                                                                      "next": {
                                                                                                                                                        "block": {
                                                                                                                                                          "type": "variables_set",
                                                                                                                                                          "id": "z,;[sgu,SQjX$`^4E3d2",
                                                                                                                                                          "fields": {
                                                                                                                                                            "VAR": {
                                                                                                                                                              "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                                            }
                                                                                                                                                          },
                                                                                                                                                          "inputs": {
                                                                                                                                                            "VALUE": {
                                                                                                                                                              "block": {
                                                                                                                                                                "type": "linalg_matrix_set",
                                                                                                                                                                "id": "g,.i/NQh4[S,UW%[pNiW",
                                                                                                                                                                "inputs": {
                                                                                                                                                                  "MATRIX": {
                                                                                                                                                                    "block": {
                                                                                                                                                                      "type": "variables_get",
                                                                                                                                                                      "id": "7Urjhko~.G+s/TtI}I^@",
                                                                                                                                                                      "fields": {
                                                                                                                                                                        "VAR": {
                                                                                                                                                                          "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                                                        }
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  },
                                                                                                                                                                  "M": {
                                                                                                                                                                    "block": {
                                                                                                                                                                      "type": "math_number",
                                                                                                                                                                      "id": "f~Qm5dgmYbo)[XVF/ME@",
                                                                                                                                                                      "fields": {
                                                                                                                                                                        "NUM": 1
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  },
                                                                                                                                                                  "N": {
                                                                                                                                                                    "block": {
                                                                                                                                                                      "type": "math_number",
                                                                                                                                                                      "id": "Ilh5z@,-RsqI7=^f8]dz",
                                                                                                                                                                      "fields": {
                                                                                                                                                                        "NUM": 2
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  },
                                                                                                                                                                  "VALUE": {
                                                                                                                                                                    "block": {
                                                                                                                                                                      "type": "math_number",
                                                                                                                                                                      "id": "1oAr1-f22oo-XNon3P|-",
                                                                                                                                                                      "fields": {
                                                                                                                                                                        "NUM": 2.223
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              }
                                                                                                                                                            }
                                                                                                                                                          },
                                                                                                                                                          "next": {
                                                                                                                                                            "block": {
                                                                                                                                                              "type": "variables_set",
                                                                                                                                                              "id": "x#}!;vk@)0pCMD|Z:lS9",
                                                                                                                                                              "fields": {
                                                                                                                                                                "VAR": {
                                                                                                                                                                  "id": "xZ(]Dq[2@`^|0HDH48We"
                                                                                                                                                                }
                                                                                                                                                              },
                                                                                                                                                              "inputs": {
                                                                                                                                                                "VALUE": {
                                                                                                                                                                  "block": {
                                                                                                                                                                    "type": "linalg_matrix_size",
                                                                                                                                                                    "id": "x^^D6Y$|O3vlE,B4~#L/",
                                                                                                                                                                    "inputs": {
                                                                                                                                                                      "MATRIX": {
                                                                                                                                                                        "block": {
                                                                                                                                                                          "type": "variables_get",
                                                                                                                                                                          "id": "*v43TBh$C,M@HuE]@$BM",
                                                                                                                                                                          "fields": {
                                                                                                                                                                            "VAR": {
                                                                                                                                                                              "id": ":3mN/aG+cW8efhRAf_OX"
                                                                                                                                                                            }
                                                                                                                                                                          }
                                                                                                                                                                        }
                                                                                                                                                                      }
                                                                                                                                                                    }
                                                                                                                                                                  }
                                                                                                                                                                }
                                                                                                                                                              }
                                                                                                                                                            }
                                                                                                                                                          }
                                                                                                                                                        }
                                                                                                                                                      }
                                                                                                                                                    }
                                                                                                                                                  }
                                                                                                                                                }
                                                                                                                                              }
                                                                                                                                            }
                                                                                                                                          }
                                                                                                                                        }
                                                                                                                                      }
                                                                                                                                    }
                                                                                                                                  }
                                                                                                                                }
                                                                                                                              }
                                                                                                                            }
                                                                                                                          }
                                                                                                                        }
                                                                                                                      }
                                                                                                                    }
                                                                                                                  }
                                                                                                                }
                                                                                                              }
                                                                                                            }
                                                                                                          }
                                                                                                        }
                                                                                                      }
                                                                                                    }
                                                                                                  }
                                                                                                }
                                                                                              }
                                                                                            }
                                                                                          }
                                                                                        }
                                                                                      }
                                                                                    }
                                                                                  }
                                                                                }
                                                                              }
                                                                            }
                                                                          }
                                                                        }
                                                                      }
                                                                    }
                                                                  }
                                                                }
                                                              }
                                                            }
                                                          }
                                                        }
                                                      }
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  },
  "variables": [
    {
      "name": "val1",
      "id": "ln~g.cb)A[bM=g#w%gi9"
    },
    {
      "name": "val2",
      "id": "{NaR7hQ5Wda5(Ws6RPF-"
    },
    {
      "name": "val3",
      "id": ":3mN/aG+cW8efhRAf_OX"
    },
    {
      "name": "val4",
      "id": "[UN{-8NrmBY+@pD(L:S["
    },
    {
      "name": "val5",
      "id": "UR8}WZnm@Nd5tWyDA,_["
    },
    {
      "name": "val6",
      "id": "xZ(]Dq[2@`^|0HDH48We"
    }
  ]
}
"""

    expected_pysrc = \
      "# Describe this function...\n" \
      "def test_linalg():\n" \
      "\n" \
      "  val1 = linalg_vector(\"3.4,5.6,7.8\")\n" \
      "  val2 = linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")\n" \
      "  val3 = linalg_fill_vector(3, val4)\n" \
      "  val3 = linalg_fill_matrix(3, 4, val4)\n" \
      "  val4 = linalg_mat_transpose(val3)\n" \
      "  val4 = linalg_mat_inv(val3)\n" \
      "  val4 = linalg_negative(val3)\n" \
      "  val4 = linalg_mat_det(val3)\n" \
      "  val4 = linalg_mat_conj(val3)\n" \
      "  val4 = linalg_mat_eigenvalues(val3)\n" \
      "  val4 = linalg_mat_eigenvectors(val3)\n" \
      "  val4 = linalg_min(val3)\n" \
      "  val4 = linalg_man(val3)\n" \
      "  val4 = linalg_argmin(val3)\n" \
      "  val4 = linalg_argmax(val3)\n" \
      "  val4 = linalg_mat_pinv(val3)\n" \
      "  val4 = linalg_mat_trace(val3)\n" \
      "  val4 = linalg_mat_diag(val3)\n" \
      "  val4 = linalg_hat(val3)\n" \
      "  val4 = linalg_sum(val3)\n" \
      "  val4 = linalg_multiply(val3)\n" \
      "  val5 = linalg_mat_add((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_mat_subtract((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_mat_multiply((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_elem_add((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_elem_subtract((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_elem_multiply((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_elem_divide((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_dot((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_cross((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val5 = linalg_mat_solve((linalg_matrix(\"[[11.2, 22.3, 44.5],[55.6,66.7,77.8]]\")), val3)\n" \
      "  val6 = linalg_vector_get_elem(val1, 2)\n" \
      "  val6 = linalg_vector_set_elem(val1, 2, 3.333)\n" \
      "  val6 = linalg_vector_len(val1)\n" \
      "  val6 = linalg_matrix_get_elem(val3, 2, 3)\n" \
      "  val6 = linalg_matrix_set_elem(val3, 1, 2, 2.223)\n" \
      "  val6 = linalg_matrix_size(val3)\n"

    _do_blockly_compile_test(linalg_blockly_json, expected_pysrc)
  

def test_blockly_compiler_geometry():
    geometry_blockly_json = \
"""
{
  "blocks": {
    "languageVersion": 0,
    "blocks": [
      {
        "type": "procedures_defnoreturn",
        "id": "aaaaa",
        "x": 20,
        "y": 20,
        "icons": {
          "comment": {
            "text": "Describe this function...",
            "pinned": false,
            "height": 80,
            "width": 160
          }
        },
        "fields": {
          "NAME": "my_procedure"
        },
        "inputs": {
          "STACK": {
            "block": {
              "type": "variables_set",
              "id": "-g;o3UC^3F6Demt8V*~c",
              "fields": {
                "VAR": {
                  "id": "O=N8TT+~l+c6jq?.4UzP"
                }
              },
              "inputs": {
                "VALUE": {
                  "block": {
                    "type": "geometry_pose_new",
                    "id": "Iki#P{H;|tCC1$Z4J:FP",
                    "inputs": {
                      "X": {
                        "block": {
                          "type": "math_number",
                          "id": "P;VNTd/,Z)9n65`k]Pmi",
                          "fields": {
                            "NUM": 12
                          }
                        }
                      },
                      "Y": {
                        "block": {
                          "type": "math_number",
                          "id": "eEzn*OG:@tuc3%eX=8%Q",
                          "fields": {
                            "NUM": 23.3
                          }
                        }
                      },
                      "Z": {
                        "block": {
                          "type": "math_number",
                          "id": "*fy`QJghWTf,9g^W(ir;",
                          "fields": {
                            "NUM": 1
                          }
                        }
                      },
                      "R_X": {
                        "block": {
                          "type": "math_number",
                          "id": "QT[b$:ms~vzv@BcGGvg_",
                          "fields": {
                            "NUM": 5
                          }
                        }
                      },
                      "R_P": {
                        "block": {
                          "type": "math_number",
                          "id": "Bkuy;.:+7y@M~g`Ve^p,",
                          "fields": {
                            "NUM": 5
                          }
                        }
                      },
                      "R_Y": {
                        "block": {
                          "type": "math_number",
                          "id": "(@2^jp)6_LvT|y7sv4uY",
                          "fields": {
                            "NUM": 2
                          }
                        }
                      }
                    }
                  }
                }
              },
              "next": {
                "block": {
                  "type": "variables_set",
                  "id": ")gWr!]EoigZf?t5bk/Mj",
                  "fields": {
                    "VAR": {
                      "id": "[lPjNQXWDZ910=yQMJpF"
                    }
                  },
                  "inputs": {
                    "VALUE": {
                      "block": {
                        "type": "geometry_pose_component_get",
                        "id": "vwh[D7Gx7,C7)os)[lKs",
                        "fields": {
                          "COMPONENT": "X"
                        },
                        "inputs": {
                          "POSE": {
                            "block": {
                              "type": "variables_get",
                              "id": "#M~`!9M$gux+k5r?9/XL",
                              "fields": {
                                "VAR": {
                                  "id": "O=N8TT+~l+c6jq?.4UzP"
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  },
                  "next": {
                    "block": {
                      "type": "variables_set",
                      "id": "Wn!qpOyj%hK4HPTe^U@W",
                      "fields": {
                        "VAR": {
                          "id": "O=N8TT+~l+c6jq?.4UzP"
                        }
                      },
                      "inputs": {
                        "VALUE": {
                          "block": {
                            "type": "geometry_pose_component_set",
                            "id": "N3L,A)#)d_9wQDqWKSgZ",
                            "fields": {
                              "COMPONENT": "X"
                            },
                            "inputs": {
                              "POSE": {
                                "block": {
                                  "type": "variables_get",
                                  "id": "pU)|.Xk/GsnAy+bm~]kh",
                                  "fields": {
                                    "VAR": {
                                      "id": "O=N8TT+~l+c6jq?.4UzP"
                                    }
                                  }
                                }
                              },
                              "VALUE": {
                                "block": {
                                  "type": "math_number",
                                  "id": "g?NFo$%%%T,5e{Ns642H",
                                  "fields": {
                                    "NUM": 2222.44444
                                  }
                                }
                              }
                            }
                          }
                        }
                      },
                      "next": {
                        "block": {
                          "type": "variables_set",
                          "id": "f-)$l5Hgk8/*Y/#hf*9]",
                          "fields": {
                            "VAR": {
                              "id": "(jy?M@5kFS=~bH7uKGTU"
                            }
                          },
                          "inputs": {
                            "VALUE": {
                              "block": {
                                "type": "geometry_pose_multiply",
                                "id": "89t5LlU^!K=wC[W%RfS]",
                                "inputs": {
                                  "A": {
                                    "block": {
                                      "type": "variables_get",
                                      "id": "%U%Hu.9Z/c=W@gX+5#r(",
                                      "fields": {
                                        "VAR": {
                                          "id": "O=N8TT+~l+c6jq?.4UzP"
                                        }
                                      }
                                    }
                                  },
                                  "B": {
                                    "block": {
                                      "type": "variables_get",
                                      "id": "c8,^VoB:C6{Af:;y`HU$",
                                      "fields": {
                                        "VAR": {
                                          "id": "O=N8TT+~l+c6jq?.4UzP"
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          },
                          "next": {
                            "block": {
                              "type": "variables_set",
                              "id": "m+r@0W|%7A[l,^2ehE3Y",
                              "fields": {
                                "VAR": {
                                  "id": "(jy?M@5kFS=~bH7uKGTU"
                                }
                              },
                              "inputs": {
                                "VALUE": {
                                  "block": {
                                    "type": "geometry_pose_inv",
                                    "id": "wE?c}`dx5[35x3$6_0R6",
                                    "inputs": {
                                      "A": {
                                        "block": {
                                          "type": "variables_get",
                                          "id": "k(ZbX6ig:9GyB$`/%hzR",
                                          "fields": {
                                            "VAR": {
                                              "id": "O=N8TT+~l+c6jq?.4UzP"
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    ]
  },
  "variables": [
    {
      "name": "var1",
      "id": "O=N8TT+~l+c6jq?.4UzP"
    },
    {
      "name": "var2",
      "id": "[lPjNQXWDZ910=yQMJpF"
    },
    {
      "name": "var3",
      "id": "(jy?M@5kFS=~bH7uKGTU"
    }
  ]
}
"""

    expected_pysrc = \
        "# Describe this function...\n" \
        "def my_procedure():\n" \
        "\n" \
        "  var1 = geometry_pose_new(12, 23.3, 1, 5, 5, 2)\n" \
        "  var2 = geometry_pose_component_get(var1, \"X\")\n" \
        "  var1 = geometry_pose_component_set(var1, \"X\", 2222.44444)\n" \
        "  var3 = geometry_pose_multiply(var1, var1)\n" \
        "  var3 = geometry_pose_inv(var1)\n"

    _do_blockly_compile_test(geometry_blockly_json, expected_pysrc)